import logging
from typing import Any
from aiogram import Router, F
from aiogram.types import Message
from app.utils.texts import TEXTS

logger = logging.getLogger("adolat_ai_bot.help_handler")
router = Router(name="help")

@router.message(F.text.in_([TEXTS["buttons"]["help"]["uz_latin"], TEXTS["buttons"]["help"]["uz_cyrillic"], TEXTS["buttons"]["help"]["ru"]]))
async def view_help(message: Message, current_user: Any):
    """Foydalanuvchi yordam va yo'riqnoma tugmasini bosganda"""
    lang = current_user.language
    await message.answer(
        text=TEXTS["help_text"][lang]
    )
