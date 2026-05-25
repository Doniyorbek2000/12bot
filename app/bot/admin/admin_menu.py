import logging
from typing import Any
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from app.config import settings
from app.utils.texts import TEXTS
from app.bot.keyboards.admin_keyboards import get_admin_menu
from app.bot.keyboards.user_keyboards import get_main_menu

logger = logging.getLogger("adolat_ai_bot.admin_menu")
router = Router(name="admin_menu")

@router.message(Command("admin"))
async def cmd_admin(message: Message, state: FSMContext, current_user: Any):
    """/admin buyrug'i faqat ADMIN_IDS dagi foydalanuvchilar uchun ishlaydi"""
    await state.clear()
    
    # Xavfsizlik tekshiruvi: telegram_id ADMIN_IDS ichida yoki roling admin/superadmin bo'lishi kerak
    if current_user.telegram_id not in settings.ADMIN_IDS and current_user.role not in ["admin", "superadmin"]:
        # Agar oddiy foydalanuvchi bo'lsa, xabar bermasdan rad etamiz yoki oddiy xabar beramiz
        await message.answer("Sizda ushbu buyruqni bajarish uchun ruxsat mavjud emas.")
        return

    await message.answer(
        text="🛠 <b>“Adolat AI” Administrator Boshqaruv Paneliga xush kelibsiz!</b>\n\nQuyidagi menyu orqali platformani to'liq nazorat qilishingiz mumkin:",
        reply_markup=get_admin_menu()
    )
    logger.info(f"Admin panelga kirdi. Admin Telegram ID: {current_user.telegram_id}")

@router.message(F.text == "🏠 Foydalanuvchi menyusi")
async def back_to_user_menu(message: Message, state: FSMContext, current_user: Any):
    """Admin foydalanuvchi menyusiga qaytganda"""
    await state.clear()
    lang = current_user.language
    await message.answer(
        text=TEXTS["main_menu_text"][lang],
        reply_markup=get_main_menu(lang)
    )
