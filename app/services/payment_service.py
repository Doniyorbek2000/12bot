import logging
import uuid
from typing import Optional, Tuple
from app.db.repositories.payment_repo import PaymentRepository
from app.db.repositories.user_repo import UserRepository
from app.db.repositories.plan_repo import PlanRepository
from app.db.models import Payment

logger = logging.getLogger("adolat_ai_bot.payment_service")

class PaymentService:
    def __init__(self, payment_repo: PaymentRepository, user_repo: UserRepository, plan_repo: PlanRepository):
        self.payment_repo = payment_repo
        self.user_repo = user_repo
        self.plan_repo = plan_repo

    async def create_invoice(self, user_id: int, plan_code: str, provider: str = "mock") -> Tuple[Optional[Payment], str]:
        """Foydalanuvchi uchun to'lov hisobi (invoice) yaratish"""
        try:
            # Plan ma'lumotlarini olish
            plan = await self.plan_repo.get_by_code(plan_code)
            if not plan:
                return None, "Tarif topilmadi"

            # Unique invoice ID yaratish
            invoice_id = f"INV-{uuid.uuid4().hex[:12].upper()}"
            
            # To'lovni pending holatda bazada saqlash
            payment = await self.payment_repo.create_payment(
                user_id=user_id,
                plan_id=plan.id,
                amount=plan.price,
                provider=provider,
                invoice_id=invoice_id
            )
            
            # Click yoki Payme uchun to'lov havolasini generatsiya qilish
            payment_url = f"https://adolat-ai.uz/pay/{invoice_id}?provider={provider}"
            
            # Agar provayder mock bo'lsa, to'g'ridan-to'g'ri test link beramiz
            if provider == "mock":
                payment_url = f"https://t.me/AdolatAIBot?start=pay_{invoice_id}"
                
            return payment, payment_url
            
        except Exception as e:
            logger.error(f"Invoice yaratishda xatolik: {e}")
            return None, f"Hisob yaratishda xatolik yuz berdi: {str(e)}"

    async def verify_and_activate_payment(self, invoice_id: str, provider_transaction_id: str, provider: str, raw_payload: Optional[dict] = None) -> Tuple[bool, str]:
        """To'lov provayderdan tasdiqlanganda chaqiriladi va foydalanuvchi tarifini yangilaydi"""
        try:
            payment = await self.payment_repo.get_by_invoice_id(invoice_id)
            if not payment:
                return False, "Hisob topilmadi"

            if payment.status == "paid":
                return True, "Hisob allaqachon to'langan"

            # To'lovni to'langan qilib belgilash
            updated_payment = await self.payment_repo.mark_as_paid(
                payment_id=payment.id,
                provider_transaction_id=provider_transaction_id,
                raw_payload=raw_payload
            )

            # Foydalanuvchiga tarifni berish
            if updated_payment:
                # Planni olish
                plan = await self.plan_repo.get_by_id(updated_payment.plan_id)
                if plan:
                    await self.user_repo.assign_plan(updated_payment.user_id, plan)
                    logger.info(f"Foydalanuvchi ID {updated_payment.user_id} uchun {plan.code} tarifi faollashtirildi.")
                    return True, "Tarif muvaffaqiyatli faollashtirildi"
            
            return False, "Tarifni yangilashda xatolik"
            
        except Exception as e:
            logger.error(f"To'lovni tasdiqlashda xatolik: {e}")
            return False, f"Xatolik: {str(e)}"
            
    async def process_mock_payment(self, invoice_id: str) -> Tuple[bool, str]:
        """Mock to'lovni sinov tariqasida darhol tasdiqlash (Testing uchun)"""
        mock_tx_id = f"MOCK-TX-{uuid.uuid4().hex[:8].upper()}"
        return await self.verify_and_activate_payment(
            invoice_id=invoice_id,
            provider_transaction_id=mock_tx_id,
            provider="mock",
            raw_payload={"mock": True}
        )
