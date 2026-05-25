import logging
from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User as TgUser
from app.db.database import AsyncSessionLocal
from app.db.repositories.user_repo import UserRepository
from app.db.repositories.plan_repo import PlanRepository
from app.db.repositories.payment_repo import PaymentRepository
from app.db.repositories.question_repo import QuestionRepository
from app.db.repositories.document_repo import DocumentRepository

logger = logging.getLogger("adolat_ai_bot.auth_middleware")

class AuthMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        # Get telegram user object from event
        tg_user: Optional[TgUser] = data.get("event_from_user")
        
        if not tg_user:
            return await handler(event, data)

        # Create async session for DB
        async with AsyncSessionLocal() as session:
            # Initialize repositories
            user_repo = UserRepository(session)
            plan_repo = PlanRepository(session)
            payment_repo = PaymentRepository(session)
            question_repo = QuestionRepository(session)
            document_repo = DocumentRepository(session)

            # Check if user is in database
            user = await user_repo.get_by_telegram_id(tg_user.id)
            if not user:
                logger.info(f"Yangi foydalanuvchi aniqlandi. Ro'yxatdan o'tkazilmoqda: {tg_user.id}")
                user = await user_repo.create_user(
                    telegram_id=tg_user.id,
                    first_name=tg_user.first_name,
                    last_name=tg_user.last_name,
                    username=tg_user.username
                )

            # Check block status
            if user.status == "blocked":
                # Bloklangan foydalanuvchilar so'rov yubora olmaydi
                if hasattr(event, "message") and event.message:
                    await event.message.answer("Siz ushbu tizimdan foydalanishdan bloklangansiz. Muammo yuzasidan adminga murojaat qiling.")
                elif hasattr(event, "callback_query") and event.callback_query:
                    await event.callback_query.answer("Siz bloklangansiz!", show_alert=True)
                return

            # Attach DB session, user object and repositories to data context for easy use in handlers
            data["db_session"] = session
            data["user_repo"] = user_repo
            data["plan_repo"] = plan_repo
            data["payment_repo"] = payment_repo
            data["question_repo"] = question_repo
            data["document_repo"] = document_repo
            data["current_user"] = user

            # Execute actual handler
            return await handler(event, data)
