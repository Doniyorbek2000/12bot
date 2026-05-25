import logging
from typing import Any
from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from app.bot.keyboards.user_keyboards import get_language_keyboard, get_main_menu
from app.utils.texts import TEXTS
from app.db.repositories.user_repo import UserRepository

logger = logging.getLogger("adolat_ai_bot.start_handler")
router = Router(name="start")

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext, current_user: Any = None):
    """/start buyrug'i kelganda ishlaydi va til tanlashni taklif qiladi"""
    await state.clear()
    
    # current_user auth middleware dan avtomatik keladi
    # Biz boshlang'ich start xabari va til tanlash klaviaturasini yuboramiz
    welcome_text = TEXTS["welcome"]["uz_latin"] # default o'zbekcha
    
    await message.answer(
        text=welcome_text,
        reply_markup=get_language_keyboard()
    )

@router.callback_query(F.data.startswith("set_lang_"))
async def callback_set_language(callback: CallbackQuery, state: FSMContext, user_repo: UserRepository, current_user: Any):
    """Foydalanuvchi til tanlaganda ishlaydi"""
    lang_code = callback.data.replace("set_lang_", "")
    
    # Bazada foydalanuvchi tilini yangilash
    await user_repo.update_language(current_user.telegram_id, lang_code)
    
    # Asosiy menyu matni
    menu_text = TEXTS["main_menu_text"][lang_code]
    
    # Callback queryga javob qaytarish va eski xabarni o'chirish
    await callback.answer()
    await callback.message.delete()
    
    # Yangi bosh menyu klaviaturasi bilan javob qaytarish
    await callback.message.answer(
        text=menu_text,
        reply_markup=get_main_menu(lang_code)
    )
    logger.info(f"Foydalanuvchi ID {current_user.telegram_id} tilni tanladi: {lang_code}")
