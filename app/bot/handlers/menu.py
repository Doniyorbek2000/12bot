import logging
from typing import Any
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from app.bot.keyboards.user_keyboards import get_language_keyboard, get_main_menu
from app.utils.texts import TEXTS

logger = logging.getLogger("adolat_ai_bot.menu_handler")
router = Router(name="menu")

@router.message(F.text.in_([TEXTS["buttons"]["change_lang"]["uz_latin"], TEXTS["buttons"]["change_lang"]["uz_cyrillic"], TEXTS["buttons"]["change_lang"]["ru"]]))
async def change_language_request(message: Message, state: FSMContext, current_user: Any):
    """Foydalanuvchi 'Tilni o'zgartirish' tugmasini bosganda ishlaydi"""
    await state.clear()
    lang = current_user.language
    await message.answer(
        text=TEXTS["welcome"][lang],
        reply_markup=get_language_keyboard()
    )

@router.message(F.text.in_([TEXTS["buttons"]["main_menu"]["uz_latin"], TEXTS["buttons"]["main_menu"]["uz_cyrillic"], TEXTS["buttons"]["main_menu"]["ru"]]))
async def go_to_main_menu(message: Message, state: FSMContext, current_user: Any):
    """Foydalanuvchi 'Bosh menyu' tugmasini bosganda ishlaydi"""
    await state.clear()
    lang = current_user.language
    await message.answer(
        text=TEXTS["main_menu_text"][lang],
        reply_markup=get_main_menu(lang)
    )

@router.callback_query(F.data == "cancel_action")
async def cancel_action_callback(callback: CallbackQuery, state: FSMContext, current_user: Any):
    """Inline bekor qilish bosilganda FSM stateni tozalaydi va bosh menyuni ochadi"""
    await state.clear()
    lang = current_user.language
    await callback.answer("Bekor qilindi")
    await callback.message.delete()
    await callback.message.answer(
        text=TEXTS["main_menu_text"][lang],
        reply_markup=get_main_menu(lang)
    )
