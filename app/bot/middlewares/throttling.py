import logging
from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message
from cachetools import TTLCache

logger = logging.getLogger("adolat_ai_bot.throttling_middleware")

class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, limit: float = 0.8):
        """
        limit: Xabarlar orasidagi minimal vaqt oralig'i (soniyalarda).
        """
        self.limit = limit
        # TTL (Time-To-Live) cache, 5 soniyalik limit kesh
        self.cache = TTLCache(maxsize=10000, ttl=5.0)

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        # Faqat Message voqealarini throttling qilamiz
        if not isinstance(event, Message):
            return await handler(event, data)

        user_id = event.from_user.id
        current_time = event.date.timestamp()

        # Foydalanuvchining oxirgi yozgan vaqtini tekshirish
        if user_id in self.cache:
            last_time = self.cache[user_id]
            if current_time - last_time < self.limit:
                # Agar foydalanuvchi limitdan tezroq yozgan bo'lsa
                logger.warning(f"Throttled: Foydalanuvchi ID {user_id} spam yubordi.")
                
                # Agar birinchi marta ogohlantirilayotgan bo'lsa
                if current_time - last_time > 0.2:
                    await event.answer("⚠️ Iltimos, xabarlarni juda tez-tez yubormang. Har bir so'rov orasida biroz kuting.")
                return

        # Yangi vaqtni yozib qo'yamiz
        self.cache[user_id] = current_time
        return await handler(event, data)
