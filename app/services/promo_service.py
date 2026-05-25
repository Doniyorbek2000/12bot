import logging
from datetime import datetime
from typing import Tuple, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import PromoCode, PromoCodeUsage, User, Plan
from app.db.repositories.user_repo import UserRepository
from app.db.repositories.plan_repo import PlanRepository

logger = logging.getLogger("adolat_ai_bot.promo_service")

class PromoService:
    def __init__(self, db: AsyncSession, user_repo: UserRepository, plan_repo: PlanRepository):
        self.db = db
        self.user_repo = user_repo
        self.plan_repo = plan_repo

    async def create_promo_code(self, code: str, discount_percent: float, plan_code: str, max_uses: int = 10, duration_days: int = 30) -> PromoCode:
        """Admin uchun yangi promo kod yaratish funksiyasi"""
        plan = await self.plan_repo.get_by_code(plan_code)
        plan_id = plan.id if plan else None
        
        from datetime import timedelta
        expires_at = datetime.utcnow() + timedelta(days=duration_days)

        promo = PromoCode(
            code=code.upper().strip(),
            discount_percent=discount_percent,
            plan_id=plan_id,
            max_uses=max_uses,
            expires_at=expires_at,
            is_active=True
        )
        self.db.add(promo)
        await self.db.commit()
        return promo

    async def use_promo_code(self, telegram_id: int, code_str: str) -> Tuple[bool, str]:
        """Foydalanuvchi promo kodni kiritganda uni tekshirish va ishlatish"""
        try:
            user = await self.user_repo.get_by_telegram_id(telegram_id)
            if not user:
                return False, "Foydalanuvchi topilmadi"

            # Promo kodni qidirish
            stmt = select(PromoCode).where(PromoCode.code == code_str.upper().strip())
            res = await self.db.execute(stmt)
            promo = res.scalars().first()

            if not promo or not promo.is_active:
                return False, "Bunday promo-kod mavjud emas yoki muddati tugagan."

            # Amal qilish muddatini tekshirish
            if promo.expires_at < datetime.utcnow():
                promo.is_active = False
                await self.db.commit()
                return False, "Promo-kodning amal qilish muddati tugagan."

            # Maksimal foydalanish sonini tekshirish
            if promo.used_count >= promo.max_uses:
                promo.is_active = False
                await self.db.commit()
                return False, "Ushbu promo-koddan foydalanish limiti tugagan."

            # Foydalanuvchi bu promo-koddan allaqachon foydalanganligini tekshirish
            stmt_usage = select(PromoCodeUsage).where(
                (PromoCodeUsage.promo_code_id == promo.id) & (PromoCodeUsage.user_id == user.id)
            )
            res_usage = await self.db.execute(stmt_usage)
            already_used = res_usage.scalars().first()
            if already_used:
                return False, "Siz ushbu promo-koddan allaqachon foydalangansiz."

            # Agar promo kod ma'lum bir tarifga (Planga) to'liq bog'langan bo'lsa va discount 100% bo'lsa (Tekin faollashtirish)
            if promo.plan_id and promo.discount_percent >= 100.0:
                plan = await self.plan_repo.get_by_id(promo.plan_id)
                if plan:
                    await self.user_repo.assign_plan(user.id, plan)
                    
                    # Log usage
                    promo.used_count += 1
                    usage = PromoCodeUsage(promo_code_id=promo.id, user_id=user.id)
                    self.db.add(usage)
                    await self.db.commit()
                    
                    return True, f"Ajoyib! Promo-kod muvaffaqiyatli ishlatildi va sizga <b>{plan.name_uz}</b> tarifi bepul taqdim etildi!"
            
            # Agar promo-kod faqat chegirma bersa
            plan = await self.plan_repo.get_by_id(promo.plan_id) if promo.plan_id else None
            plan_name = plan.name_uz if plan else "istalgan tarif"
            return True, f"Ushbu promo-kod tasdiqlandi. Siz {plan_name} uchun <b>{promo.discount_percent}% chegirma</b> oldingiz! To'lov vaqtida chegirma avtomatik hisoblanadi."

        except Exception as e:
            logger.error(f"Promo kod ishlatishda xatolik: {e}")
            return False, f"Xatolik yuz berdi: {str(e)}"
