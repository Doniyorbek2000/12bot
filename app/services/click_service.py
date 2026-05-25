import hashlib
import logging
from typing import dict
from app.config import settings
from app.services.payment_service import PaymentService

logger = logging.getLogger("adolat_ai_bot.click_service")

class ClickService:
    def __init__(self, payment_service: PaymentService):
        self.payment_service = payment_service
        self.secret_key = settings.CLICK_SECRET_KEY
        self.service_id = settings.CLICK_SERVICE_ID

    def generate_signature(self, click_trans_id: str, merchant_trans_id: str, amount: str, action: str, sign_time: str) -> str:
        """Click oqimi spetsifikatsiyasiga asosan MD5 imzo yaratish"""
        sign_string = f"{click_trans_id}{self.service_id}{self.secret_key}{merchant_trans_id}{amount}{action}{sign_time}"
        return hashlib.md5(sign_string.encode('utf-8')).hexdigest()

    async def process_webhook(self, payload: dict) -> dict:
        """
        Click webhook (Prepare va Complete) so'rovlarini qayta ishlash.
        Spetsifikatsiya bo'yicha javob beradi:
        {
          "click_trans_id": X,
          "merchant_trans_id": Y,
          "merchant_prepare_id": Z, # Prepare uchun
          "merchant_confirm_id": W, # Complete uchun
          "error": 0,
          "error_note": "Success"
        }
        """
        click_trans_id = str(payload.get("click_trans_id", ""))
        merchant_trans_id = str(payload.get("merchant_trans_id", ""))
        amount = str(payload.get("amount", ""))
        action = str(payload.get("action", ""))
        sign_time = str(payload.get("sign_time", ""))
        signature = str(payload.get("sign_string", ""))
        
        # 1. Signature validation
        expected_sig = self.generate_signature(click_trans_id, merchant_trans_id, amount, action, sign_time)
        if signature != expected_sig:
            logger.error(f"Click xavfsizlik imzosi mos kelmadi. Kutilgan: {expected_sig}, Kelgan: {signature}")
            return {
                "error": -1, # Signature error
                "error_note": "Signature verification failed"
            }

        # 2. Actionlar
        # Action = 0: Prepare request (hisobni tekshirish va to'lovni kutish)
        if action == "0":
            # Merchant trans (bizdagi invoice_id) mavjudligini tekshiramiz
            payment = await self.payment_service.payment_repo.get_by_invoice_id(merchant_trans_id)
            if not payment:
                return {"error": -5, "error_note": "User or Invoice not found"}
            if payment.amount != float(amount):
                return {"error": -2, "error_note": "Incorrect amount"}
            
            return {
                "click_trans_id": click_trans_id,
                "merchant_trans_id": merchant_trans_id,
                "merchant_prepare_id": payment.id,
                "error": 0,
                "error_note": "Success"
            }
            
        # Action = 1: Complete request (to'lov muvaffaqiyatli bajarildi)
        elif action == "1":
            payment = await self.payment_service.payment_repo.get_by_invoice_id(merchant_trans_id)
            if not payment:
                return {"error": -5, "error_note": "Invoice not found"}
                
            # To'lovni tasdiqlash va tarifni faollashtirish
            success, message = await self.payment_service.verify_and_activate_payment(
                invoice_id=merchant_trans_id,
                provider_transaction_id=click_trans_id,
                provider="click",
                raw_payload=payload
            )
            
            if success:
                return {
                    "click_trans_id": click_trans_id,
                    "merchant_trans_id": merchant_trans_id,
                    "merchant_confirm_id": payment.id,
                    "error": 0,
                    "error_note": "Success"
                }
            else:
                return {
                    "error": -9,
                    "error_note": f"Transaction failed to confirm: {message}"
                }
                
        return {"error": -3, "error_note": "Action not found"}
