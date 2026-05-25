from datetime import datetime, time
from typing import List, Optional
from sqlalchemy import select, delete, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import Question

class QuestionRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_question(self, user_id: int, question_text: str, answer_text: str, language: str, model_name: str, tokens_input: int = 0, tokens_output: int = 0, status: str = "success") -> Question:
        question = Question(
            user_id=user_id,
            question_text=question_text,
            answer_text=answer_text,
            language=language,
            model_name=model_name,
            tokens_input=tokens_input,
            tokens_output=tokens_output,
            status=status
        )
        self.db.add(question)
        await self.db.commit()
        return question

    async def get_history_by_user(self, user_id: int, limit: int = 10) -> List[Question]:
        stmt = select(Question).where(Question.user_id == user_id).order_by(Question.created_at.desc()).limit(limit)
        res = await self.db.execute(stmt)
        return list(res.scalars().all())

    async def clear_history(self, user_id: int) -> None:
        stmt = delete(Question).where(Question.user_id == user_id)
        await self.db.execute(stmt)
        await self.db.commit()

    async def get_total_count(self) -> int:
        stmt = select(func.count(Question.id))
        res = await self.db.execute(stmt)
        return res.scalar() or 0

    async def get_today_count(self) -> int:
        today_start = datetime.combine(datetime.utcnow().date(), time.min)
        stmt = select(func.count(Question.id)).where(Question.created_at >= today_start)
        res = await self.db.execute(stmt)
        return res.scalar() or 0
