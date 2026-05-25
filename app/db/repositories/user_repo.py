from datetime import datetime, timedelta
from typing import Optional, List, Tuple
from sqlalchemy import select, update, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.db.models import User, Plan, UsageCounter

class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_telegram_id(self, telegram_id: int) -> Optional[User]:
        stmt = (
            select(User)
            .where(User.telegram_id == telegram_id)
            .options(
                selectinload(User.plan),
                selectinload(User.usage_counter)
            )
        )
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def get_by_id(self, user_id: int) -> Optional[User]:
        stmt = (
            select(User)
            .where(User.id == user_id)
            .options(
                selectinload(User.plan),
                selectinload(User.usage_counter)
            )
        )
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def create_user(self, telegram_id: int, first_name: str, last_name: Optional[str] = None, username: Optional[str] = None) -> User:
        # Default Plan FREE bo'lishi kerak. Avval FREE plan borligini tekshiramiz.
        stmt_plan = select(Plan).where(Plan.code == "FREE")
        res_plan = await self.db.execute(stmt_plan)
        free_plan = res_plan.scalars().first()
        free_plan_id = free_plan.id if free_plan else None

        user = User(
            telegram_id=telegram_id,
            first_name=first_name,
            last_name=last_name,
            username=username,
            current_plan_id=free_plan_id,
            plan_started_at=datetime.utcnow(),
            plan_expires_at=datetime.utcnow() + timedelta(days=365) # FREE plan 1 yil
        )
        self.db.add(user)
        await self.db.flush()

        # UsageCounter yaratish
        counter = UsageCounter(
            user_id=user.id,
            period_start=datetime.utcnow(),
            period_end=datetime.utcnow() + timedelta(days=30)
        )
        self.db.add(counter)
        await self.db.commit()
        
        # Userni qayta yuklash (plan va counter bilan birga)
        return await self.get_by_telegram_id(telegram_id)

    async def update_language(self, telegram_id: int, language: str) -> None:
        stmt = update(User).where(User.telegram_id == telegram_id).values(language=language)
        await self.db.execute(stmt)
        await self.db.commit()

    async def update_status(self, telegram_id: int, status: str) -> None:
        stmt = update(User).where(User.telegram_id == telegram_id).values(status=status)
        await self.db.execute(stmt)
        await self.db.commit()

    async def update_role(self, telegram_id: int, role: str) -> None:
        stmt = update(User).where(User.telegram_id == telegram_id).values(role=role)
        await self.db.execute(stmt)
        await self.db.commit()

    async def assign_plan(self, user_id: int, plan: Plan) -> User:
        user = await self.get_by_id(user_id)
        if user:
            user.current_plan_id = plan.id
            user.plan_started_at = datetime.utcnow()
            user.plan_expires_at = datetime.utcnow() + timedelta(days=plan.duration_days)
            
            # Counter-ni ham reset qilamiz
            if user.usage_counter:
                user.usage_counter.period_start = datetime.utcnow()
                user.usage_counter.period_end = user.plan_expires_at
                user.usage_counter.questions_used = 0
                user.usage_counter.document_analysis_used = 0
                user.usage_counter.document_generation_used = 0
                user.usage_counter.voice_minutes_used = 0
            
            await self.db.commit()
        return user

    async def search_users(self, query: str) -> List[User]:
        stmt = (
            select(User)
            .where(
                (User.first_name.ilike(f"%{query}%")) | 
                (User.username.ilike(f"%{query}%")) |
                (func.cast(User.telegram_id, String).ilike(f"%{query}%"))
            )
            .limit(10)
        )
        res = await self.db.execute(stmt)
        return list(res.scalars().all())
