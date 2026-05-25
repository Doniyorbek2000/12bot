import base64
import logging
import time
from typing import Optional, dict
from app.config import settings
from app.services.payment_service import PaymentService

logger = logging.getLogger("adolat_ai_bot.payme_service")

class PaymeService:
    def __init__(self, payment_service: PaymentService):
        self.payment_service = payment_service
        self.merchant_key = settings.PAYME_SECRET_KEY

    def verify_auth(self, auth_header: str) -> bool:
        """Payme Basic Auth sarlavhasini tekshirish"""
        if not auth_header or not auth_header.startswith("Basic "):
            return False
        
        try:
            encoded_key = auth_header.split(" ")[1]
            decoded = base64.b64decode(encoded_key).decode("utf-8")
            # Payme odatda "Paycom:key" formatida yuboradi
            parts = decoded.split(":")
            if len(parts) >= 2:
                key = parts[1]
                return key == self.merchant_key
            return decoded == self.merchant_key
        except Exception as e:
            logger.error(f"Payme auth tekshiruvida xatolik: {e}")
            return False

    async def process_rpc_request(self, rpc_request: dict) -> dict:
        """
        Payme JSON-RPC 2.0 spetsifikatsiyasi bo'yicha so'rovlarni boshqarish
        """
        method = rpc_request.get("method")
        params = rpc_request.get("params", {})
        request_id = rpc_request.get("id")

        if method == "CheckPerformTransaction":
            return await self._check_perform_transaction(params, request_id)
        elif method == "CreateTransaction":
            return await self._create_transaction(params, request_id)
        elif method == "PerformTransaction":
            return await self._perform_transaction(params, request_id)
        elif method == "CancelTransaction":
            return await self._cancel_transaction(params, request_id)
        elif method == "CheckTransaction":
            return await self._check_transaction(params, request_id)
            
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "error": {
                "code": -32601,
                "message": "Method not found"
            }
        }

    async def _check_perform_transaction(self, params: dict, request_id: int) -> dict:
        amount = params.get("amount") # tiyinlarda keladi (1 so'm = 100 tiyin)
        account = params.get("account", {})
        invoice_id = account.get("invoice_id")

        payment = await self.payment_service.payment_repo.get_by_invoice_id(invoice_id)
        if not payment:
            return self._rpc_error(-31050, "Invoice not found", request_id)
        
        # Paymedagi tiyin miqdorini solishtirish
        expected_tiyin = int(payment.amount * 100)
        if expected_tiyin != int(amount):
            return self._rpc_error(-31001, "Incorrect amount", request_id)

        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "allow": True
            }
        }

    async def _create_transaction(self, params: dict, request_id: int) -> dict:
        tx_id = params.get("id")
        amount = params.get("amount")
        account = params.get("account", {})
        invoice_id = account.get("invoice_id")
        
        payment = await self.payment_service.payment_repo.get_by_invoice_id(invoice_id)
        if not payment:
            return self._rpc_error(-31050, "Invoice not found", request_id)
            
        expected_tiyin = int(payment.amount * 100)
        if expected_tiyin != int(amount):
            return self._rpc_error(-31001, "Incorrect amount", request_id)

        # Agar tranzaksiya allaqachon mavjud bo'lsa
        existing = await self.payment_service.payment_repo.get_by_provider_transaction_id("payme", tx_id)
        if existing:
            if existing.status == "paid":
                return self._rpc_error(-31080, "Transaction already paid", request_id)
            
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "create_time": int(existing.created_at.timestamp() * 1000),
                    "transaction": str(existing.id),
                    "state": 1 # 1 = In progress
                }
            }

        # Tranzaksiya haqidagi ma'lumotlarni yangilab qo'yamiz (baza payments jadvalida provider_transaction_id o'rnatiladi)
        payment.provider_transaction_id = tx_id
        payment.provider = "payme"
        payment.raw_payload_json = params
        await self.payment_service.payment_repo.db.commit()

        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "create_time": int(time.time() * 1000),
                "transaction": str(payment.id),
                "state": 1
            }
        }

    async def _perform_transaction(self, params: dict, request_id: int) -> dict:
        tx_id = params.get("id")
        
        payment = await self.payment_service.payment_repo.get_by_provider_transaction_id("payme", tx_id)
        if not payment:
            return self._rpc_error(-31003, "Transaction not found", request_id)

        if payment.status == "paid":
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "perform_time": int(payment.paid_at.timestamp() * 1000) if payment.paid_at else int(time.time() * 1000),
                    "transaction": str(payment.id),
                    "state": 2 # 2 = Completed
                }
            }

        # To'lovni tasdiqlash
        success, message = await self.payment_service.verify_and_activate_payment(
            invoice_id=payment.invoice_id,
            provider_transaction_id=tx_id,
            provider="payme",
            raw_payload=params
        )

        if success:
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "perform_time": int(time.time() * 1000),
                    "transaction": str(payment.id),
                    "state": 2
                }
            }
        else:
            return self._rpc_error(-31008, f"Activation error: {message}", request_id)

    async def _cancel_transaction(self, params: dict, request_id: int) -> dict:
        tx_id = params.get("id")
        reason = params.get("reason")

        payment = await self.payment_service.payment_repo.get_by_provider_transaction_id("payme", tx_id)
        if not payment:
            return self._rpc_error(-31003, "Transaction not found", request_id)

        if payment.status == "cancelled":
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "cancel_time": int(payment.created_at.timestamp() * 1000),
                    "transaction": str(payment.id),
                    "state": -1 # -1 = Cancelled
                }
            }

        # To'lovni bekor qilish
        payment.status = "cancelled"
        payment.raw_payload_json = {"reason": reason, "cancelled_at": time.time()}
        await self.payment_service.payment_repo.db.commit()

        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "cancel_time": int(time.time() * 1000),
                "transaction": str(payment.id),
                "state": -1
            }
        }

    async def _check_transaction(self, params: dict, request_id: int) -> dict:
        tx_id = params.get("id")
        payment = await self.payment_service.payment_repo.get_by_provider_transaction_id("payme", tx_id)
        if not payment:
            return self._rpc_error(-31003, "Transaction not found", request_id)

        state = 1
        if payment.status == "paid":
            state = 2
        elif payment.status == "cancelled":
            state = -1

        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "create_time": int(payment.created_at.timestamp() * 1000),
                "perform_time": int(payment.paid_at.timestamp() * 1000) if payment.paid_at else 0,
                "cancel_time": 0 if payment.status != "cancelled" else int(time.time() * 1000),
                "transaction": str(payment.id),
                "state": state,
                "reason": None
            }
        }

    def _rpc_error(self, code: int, message: str, request_id: int) -> dict:
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "error": {
                "code": code,
                "message": message
            }
        }
