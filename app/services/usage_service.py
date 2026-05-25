import logging
from datetime import datetime, timedelta
from typing import Tuple, Optional
from app.db.repositories.user_repo import UserRepository
from app.db.repositories.plan_repo import PlanRepository
from app.db.models import User, Plan, UsageCounter

logger = logging.getLogger("adolat_ai_bot.usage_service")

class UsageService:
    def __init__(self, user_repo: UserRepository, plan_repo: PlanRepository):
        self.user_repo = user_repo
        self.plan_repo = plan_repo

    async def get_or_check_user_limits(self, telegram_id: int) -> Tuple[User, Plan, UsageCounter]:
        """Foydalanuvchi ma'lumotlarini yuklaydi va tarif muddati tugagan bo'lsa downgrade qiladi"""
        user = await self.user_repo.get_by_telegram_id(telegram_id)
        if not user:
            raise ValueError("Foydalanuvchi topilmadi")

        # 1. Tarif muddati tugaganligini tekshirish
        if user.plan_expires_at and user.plan_expires_at < datetime.utcnow() and user.plan.code != "FREE":
            logger.info(f"Foydalanuvchi ID {user.id} tarifi muddati tugadi. FREE tarifga tushirilmoqda.")
            free_plan = await self.plan_repo.get_by_code("FREE")
            if free_plan:
                user = await self.user_repo.assign_plan(user.id, free_plan)

        plan = user.plan
        counter = user.usage_counter

        # 2. Agar usage counter muddati tugagan bo'lsa (masalan: 30 kunlik davr)
        if counter and counter.period_end < datetime.utcnow():
            logger.info(f"Foydalanuvchi ID {user.id} limit hisoblagich davri tugadi. Limitlar yangilanmoqda.")
            counter.period_start = datetime.utcnow()
            counter.period_end = datetime.utcnow() + timedelta(days=30)
            counter.questions_used = 0
            counter.document_analysis_used = 0
            counter.document_generation_used = 0
            counter.voice_minutes_used = 0
            await self.user_repo.db.commit()

        return user, plan, counter

    async def can_ask_question(self, telegram_id: int) -> Tuple[bool, str]:
        """Foydalanuvchi savol berish limitini tekshirish va kamaytirish"""
        user, plan, counter = await self.get_or_check_user_limits(telegram_id)
        
        if counter.questions_used >= plan.question_limit:
            return False, f"Sizning joriy tarifingiz bo'yicha huquqiy savollar limiti tugagan. Limit: {plan.question_limit} ta."

        # Limitni oshirish
        counter.questions_used += 1
        await self.user_repo.db.commit()
        return True, "Ruxsat etildi"

    async def can_analyze_document(self, telegram_id: int, file_size_bytes: int) -> Tuple[bool, str]:
        """Foydalanuvchi hujjat tahlil qilish limitini va fayl hajmini tekshirish"""
        user, plan, counter = await self.get_or_check_user_limits(telegram_id)

        # 1. Hujjat tahlili sonini tekshirish
        if counter.document_analysis_used >= plan.document_analysis_limit:
            return False, f"Sizning joriy tarifingiz bo'yicha hujjat tahlili limiti tugagan. Limit: {plan.document_analysis_limit} ta."

        # 2. Fayl hajmini tekshirish
        max_size_bytes = plan.max_file_size_mb * 1024 * 1024
        if file_size_bytes > max_size_bytes:
            return False, f"Sizning tarifingiz bo'yicha ruxsat berilgan maksimal fayl hajmi: {plan.max_file_size_mb} MB. Siz yuborgan fayl hajmi juda katta."

        # Limitni oshirish
        counter.document_analysis_used += 1
        await self.user_repo.db.commit()
        return True, "Ruxsat etildi"

    async def can_generate_document(self, telegram_id: int) -> Tuple[bool, str]:
        """Foydalanuvchi yangi hujjat yaratish limitini tekshirish va kamaytirish"""
        user, plan, counter = await self.get_or_check_user_limits(telegram_id)

        if counter.document_generation_used >= plan.document_generation_limit:
            return False, f"Sizning joriy tarifingiz bo'yicha hujjat yaratish limiti tugagan. Limit: {plan.document_generation_limit} ta."

        # Limitni oshirish
        counter.document_generation_used += 1
        await self.user_repo.db.commit()
        return True, "Ruxsat etildi"

    async def can_use_voice(self, telegram_id: int, duration_seconds: int = 10) -> Tuple[bool, str]:
        """Foydalanuvchi ovozli xabar limitini tekshirish"""
        user, plan, counter = await self.get_or_check_user_limits(telegram_id)

        duration_minutes = duration_seconds / 60.0
        
        if plan.voice_limit_minutes == 0:
            return False, "Sizning joriy FREE/ODDIY tarifingizda ovozli xizmat mavjud emas. Iltimos, PRO yoki undan yuqori tarifga o'ting."

        if counter.voice_minutes_used + duration_minutes > plan.voice_limit_minutes:
            return False, f"Sizning ovozli so'rovlar limitingiz tugagan. Qolgan: {max(0.0, plan.voice_limit_minutes - counter.voice_minutes_used):.1f} daqiqa."

        # Limitni oshirish
        counter.voice_minutes_used += duration_minutes
        await self.user_repo.db.commit()
        return True, "Ruxsat etildi"
