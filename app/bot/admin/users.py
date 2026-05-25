import logging
from typing import Any
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from app.config import settings
from app.bot.states.admin_states import AdminStates
from app.bot.keyboards.admin_keyboards import get_user_manage_keyboard, get_admin_plans_keyboard, get_admin_menu
from app.db.repositories.user_repo import UserRepository
from app.db.repositories.plan_repo import PlanRepository
from app.db.repositories.audit_repo import AuditRepository

logger = logging.getLogger("adolat_ai_bot.admin_users")
router = Router(name="admin_users")

@router.message(F.text == "👥 Foydalanuvchilar")
async def admin_users_search_start(message: Message, state: FSMContext, current_user: Any):
    """Admin foydalanuvchilar bo'limini bosganda"""
    if current_user.telegram_id not in settings.ADMIN_IDS and current_user.role not in ["admin", "superadmin"]:
        return
        
    await state.set_state(AdminStates.searching_user)
    await message.answer("👥 <b>Foydalanuvchilarni boshqarish:</b>\n\nIltimos, qidirilayotgan foydalanuvchining Telegram ID raqamini yoki username'ini yozib yuboring:")

@router.message(AdminStates.searching_user)
async def process_user_search(message: Message, state: FSMContext, current_user: Any, user_repo: UserRepository):
    """Admin foydalanuvchini qidiruv so'rovini yuborganda"""
    if current_user.telegram_id not in settings.ADMIN_IDS and current_user.role not in ["admin", "superadmin"]:
        return
        
    query = message.text.strip()
    
    # Bekor qilish yoki orqaga qaytish tugmalari bo'lsa
    if query in ["🏠 Foydalanuvchi menyusi", "📊 Dashboard"]:
        await state.clear()
        return

    users = await user_repo.search_users(query)
    
    if not users:
        await message.answer("❌ Mos keladigan foydalanuvchi topilmadi. Qayta urinib ko'ring yoki boshqa ma'lumot yuboring:")
        return

    await state.clear()
    
    for u in users:
        # User profili va boshqaruv inline tugmasi
        is_blocked = u.status == "blocked"
        
        status_emoji = "🟢 Faol" if u.status == "active" else "🔴 Bloklangan"
        
        profile_text = (
            "👤 <b>Foydalanuvchi Profili (Admin ko'rinishi):</b>\n\n"
            "• ID: <code>{u_id}</code>\n"
            "• Telegram ID: <code>{tg_id}</code>\n"
            "• F.I.Sh: <b>{first_name} {last_name}</b>\n"
            "• Username: @{username}\n"
            "• Til: <code>{lang}</code>\n"
            "• Rol: <b>{role}</b>\n"
            "• Holat: {status}\n"
            "• Joriy plan: <b>{plan_code}</b>\n"
            "• Ro'yxatdan o'tdi: <code>{created_at}</code>\n"
        ).format(
            u_id=u.id, tg_id=u.telegram_id,
            first_name=u.first_name, last_name=u.last_name or "",
            username=u.username or "yo'q",
            lang=u.language, role=u.role, status=status_emoji,
            plan_code=u.plan.code if u.plan else "yo'q",
            created_at=u.created_at.strftime("%d.%m.%Y %H:%M")
        )
        
        await message.answer(
            text=profile_text,
            reply_markup=get_user_manage_keyboard(u.telegram_id, is_blocked)
        )

@router.callback_query(F.data.startswith("admin_block_user_"))
async def callback_admin_block(callback: CallbackQuery, user_repo: UserRepository, audit_repo: AuditRepository, current_user: Any):
    """Admin foydalanuvchini bloklaganda"""
    if current_user.telegram_id not in settings.ADMIN_IDS and current_user.role not in ["admin", "superadmin"]:
        return
        
    target_tg_id = int(callback.data.replace("admin_block_user_", ""))
    
    # Bloklash
    await user_repo.update_status(target_tg_id, "blocked")
    
    # Audit log
    await audit_repo.log_action(
        admin_id=current_user.telegram_id,
        action="block_user",
        entity_type="user",
        entity_id=target_tg_id,
        old_value_json={"status": "active"},
        new_value_json={"status": "blocked"}
    )

    await callback.answer("Foydalanuvchi bloklandi", show_alert=True)
    await callback.message.delete()

@router.callback_query(F.data.startswith("admin_unblock_user_"))
async def callback_admin_unblock(callback: CallbackQuery, user_repo: UserRepository, audit_repo: AuditRepository, current_user: Any):
    """Admin foydalanuvchini blokdan chiqarganda"""
    if current_user.telegram_id not in settings.ADMIN_IDS and current_user.role not in ["admin", "superadmin"]:
        return
        
    target_tg_id = int(callback.data.replace("admin_unblock_user_", ""))
    
    # Blokdan chiqarish
    await user_repo.update_status(target_tg_id, "active")
    
    # Audit log
    await audit_repo.log_action(
        admin_id=current_user.telegram_id,
        action="unblock_user",
        entity_type="user",
        entity_id=target_tg_id,
        old_value_json={"status": "blocked"},
        new_value_json={"status": "active"}
    )

    await callback.answer("Foydalanuvchi blokdan chiqarildi", show_alert=True)
    await callback.message.delete()

@router.callback_query(F.data.startswith("admin_give_plan_"))
async def callback_admin_give_plan_start(callback: CallbackQuery, state: FSMContext, current_user: Any):
    """Admin foydalanuvchiga tarif biriktirish tugmasini bosganda"""
    if current_user.telegram_id not in settings.ADMIN_IDS and current_user.role not in ["admin", "superadmin"]:
        return
        
    target_tg_id = int(callback.data.replace("admin_give_plan_", ""))
    await state.update_data(target_user_tg_id=target_tg_id)
    
    await callback.answer()
    await callback.message.answer(
        text="🧾 Biriktiriladigan tarifni tanlang:",
        reply_markup=get_admin_plans_keyboard()
    )

@router.callback_query(F.data.startswith("admin_assign_plan_"))
async def callback_admin_assign_plan(callback: CallbackQuery, state: FSMContext, user_repo: UserRepository, plan_repo: PlanRepository, audit_repo: AuditRepository, current_user: Any):
    """Admin yangi tarifni tanlaganda"""
    if current_user.telegram_id not in settings.ADMIN_IDS and current_user.role not in ["admin", "superadmin"]:
        return
        
    plan_code = callback.data.replace("admin_assign_plan_", "")
    
    state_data = await state.get_data()
    target_tg_id = state_data.get("target_user_tg_id")
    
    await state.clear()
    await callback.message.delete()
    
    if not target_tg_id:
        await callback.answer("Xatolik: Foydalanuvchi ID topilmadi", show_alert=True)
        return

    # Foydalanuvchi va Planlarni olish
    target_user = await user_repo.get_by_telegram_id(target_tg_id)
    plan = await plan_repo.get_by_code(plan_code)
    
    if target_user and plan:
        old_plan_code = target_user.plan.code if target_user.plan else "FREE"
        
        # Yangi plan biriktirish
        await user_repo.assign_plan(target_user.id, plan)
        
        # Audit log
        await audit_repo.log_action(
            admin_id=current_user.telegram_id,
            action="assign_plan",
            entity_type="user",
            entity_id=target_user.id,
            old_value_json={"plan": old_plan_code},
            new_value_json={"plan": plan_code}
        )
        
        await callback.answer(f"Foydalanuvchiga {plan_code} tarifi qo'yildi", show_alert=True)
    else:
        await callback.answer("Xatolik yuz berdi", show_alert=True)
