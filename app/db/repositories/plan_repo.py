from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import Plan

class PlanRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all_active(self) -> List[Plan]:
        stmt = select(Plan).where(Plan.is_active == True).order_by(Plan.price.asc())
        res = await self.db.execute(stmt)
        return list(res.scalars().all())

    async def get_by_code(self, code: str) -> Optional[Plan]:
        stmt = select(Plan).where(Plan.code == code)
        res = await self.db.execute(stmt)
        return res.scalars().first()

    async def get_by_id(self, plan_id: int) -> Optional[Plan]:
        stmt = select(Plan).where(Plan.id == plan_id)
        res = await self.db.execute(stmt)
        return res.scalars().first()

    async def seed_plans(self) -> None:
        """Standart tariflarni bazaga birinchi marta yozish"""
        plans_data = [
            {
                "code": "FREE",
                "name_uz": "FREE (Tekin)",
                "name_ru": "FREE (Бесплатно)",
                "price": 0.0,
                "question_limit": 2,
                "document_analysis_limit": 1,
                "document_generation_limit": 1,
                "voice_limit_minutes": 0,
                "max_file_size_mb": 1,
                "duration_days": 365,
                "is_active": True
            },
            {
                "code": "ODDIY",
                "name_uz": "ODDIY",
                "name_ru": "ОБЫЧНЫЙ",
                "price": 50000.0,
                "question_limit": 50,
                "document_analysis_limit": 10,
                "document_generation_limit": 10,
                "voice_limit_minutes": 0,
                "max_file_size_mb": 5,
                "duration_days": 30,
                "is_active": True
            },
            {
                "code": "PRO",
                "name_uz": "PRO (Ovozli)",
                "name_ru": "PRO (Голосовой)",
                "price": 120000.0,
                "question_limit": 200,
                "document_analysis_limit": 50,
                "document_generation_limit": 50,
                "voice_limit_minutes": 60,
                "max_file_size_mb": 20,
                "duration_days": 30,
                "is_active": True
            },
            {
                "code": "STANDART",
                "name_uz": "STANDART",
                "name_ru": "СТАНДАРТ",
                "price": 500000.0,
                "question_limit": 1000,
                "document_analysis_limit": 200,
                "document_generation_limit": 150,
                "voice_limit_minutes": 300,
                "max_file_size_mb": 50,
                "duration_days": 30,
                "is_active": True
            },
            {
                "code": "ULTRA",
                "name_uz": "ULTRA",
                "name_ru": "УЛЬТРА",
                "price": 1200000.0,
                "question_limit": 5000,
                "document_analysis_limit": 500,
                "document_generation_limit": 400,
                "voice_limit_minutes": 1000,
                "max_file_size_mb": 100,
                "duration_days": 30,
                "is_active": True
            },
            {
                "code": "VIP",
                "name_uz": "VIP (Premium)",
                "name_ru": "VIP (Премиум)",
                "price": 5000000.0,
                "question_limit": 99999,
                "document_analysis_limit": 9999,
                "document_generation_limit": 9999,
                "voice_limit_minutes": 9999,
                "max_file_size_mb": 500,
                "duration_days": 90,
                "is_active": True
            }
        ]

        for plan_info in plans_data:
            stmt = select(Plan).where(Plan.code == plan_info["code"])
            res = await self.db.execute(stmt)
            existing = res.scalars().first()
            if not existing:
                plan = Plan(**plan_info)
                self.db.add(plan)
        
        await self.db.commit()
