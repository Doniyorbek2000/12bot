import logging
from typing import Any
from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from app.config import settings
from app.bot.keyboards.admin_keyboards import get_payment_approval_keyboard
from app.services.payment_service import PaymentService
from app.db.repositories.payment_repo import PaymentRepository
from app.db.repositories.user_repo import UserRepository
from app.db.repositories.plan_repo import PlanRepository
from app.db.repositories.audit_repo import AuditRepository

logger = logging.getLogger("adolat_ai_bot.admin_payments")
router = Router(name="admin_payments")

@router.message(F.text == "💳 To'lovlar")
async def admin_view_payments(message: Message, current_user: Any, payment_repo: PaymentRepository):
    """Admin to'lovlar ro'yxatini ko'rish tugmasini bosganda"""
    if current_user.telegram_id not in settings.ADMIN_IDS and current_user.role not in ["admin", "superadmin"]:
        return

    payments = await payment_repo.get_all_payments()
    
    if not payments:
        await message.answer("💳 Hozircha hech qanday to'lovlar amalga oshirilmagan.")
        return

    await message.answer("💳 <b>Tizimdagi to'lovlar (Oxirgi 15 ta):</b>")
    
    # Faqat oxirgi 15 ta to'lovni ko'rsatamiz chat to'lib ketmasligi uchun
    for pay in payments[:15]:
        status_emoji = {
            "pending": "⏳ Kutilmoqda",
            "paid": "🟢 To'langan",
            "failed": "🔴 Muvaffaqiyatsiz",
            "cancelled": "⚫ Bekor qilingan"
        }.get(pay.status, pay.status)
        
        user_info = f"@{pay.user.username}" if pay.user.username else pay.user.first_name
        
        pay_text = (
            "🧾 <b>To'lov ma'lumotlari:</b>\n"
            "• Invoice ID: <code>{inv_id}</code>\n"
            "• Foydalanuvchi: <b>{user}</b> (ID: <code>{tg_id}</code>)\n"
            "• Tarif: <b>{plan_code}</b>\n"
            "• Summa: <b>{amount:,.0f} so'm</b>\n"
            "• Provayder: <code>{provider}</code>\n"
            "• Status: {status}\n"
            "• Yaratilgan sana: <code>{date}</code>\n"
        ).format(
            inv_id=pay.invoice_id, user=user_info, tg_id=pay.user.telegram_id,
            plan_code=pay.plan.code, amount=pay.amount, provider=pay.provider.upper(),
            status=status_emoji, date=pay.created_at.strftime("%d.%m.%Y %H:%M")
        )
        
        # Agar status pending bo'lsa admin qo'lda tasdiqlay oladi
        markup = get_payment_approval_keyboard(pay.invoice_id) if pay.status == "pending" else None
        
        await message.answer(text=pay_text, reply_markup=markup)

@router.callback_query(F.data.startswith("admin_approve_pay_"))
async def callback_admin_approve_payment(callback: CallbackQuery, bot: Bot, payment_repo: PaymentRepository, plan_repo: PlanRepository, audit_repo: AuditRepository, current_user: Any):
    """Admin to'lovni inline tasdiqlaganda"""
    if current_user.telegram_id not in settings.ADMIN_IDS and current_user.role not in ["admin", "superadmin"]:
        return

    invoice_id = callback.data.replace("admin_approve_pay_", "")
    
    # PaymentService orqali to'lovni tasdiqlash va faollashtirish
    user_repo = UserRepository(payment_repo.db)
    payment_service = PaymentService(payment_repo, user_repo, plan_repo)
    
    # Tranzaksiya ID sifatida qo'lda tasdiqlangnini belgilaymiz
    manual_tx_id = f"MANUAL-APPROVED-BY-{current_user.telegram_id}"
    
    success, message = await payment_service.verify_and_activate_payment(
        invoice_id=invoice_id,
        provider_transaction_id=manual_tx_id,
        provider="manual",
        raw_payload={"admin_approver": current_user.telegram_id}
    )

    if success:
        # Audit log yozish
        await audit_repo.log_action(
            admin_id=current_user.telegram_id,
            action="manual_approve_payment",
            entity_type="payment",
            entity_id=None,
            old_value_json={"invoice_id": invoice_id, "status": "pending"},
            new_value_json={"status": "paid", "approver": current_user.telegram_id}
        )
        
        # Foydalanuvchiga xabar yuborish
        # Avval to'lovni yuklab olib telegram_id sini aniqlaymiz
        payment = await payment_repo.get_by_invoice_id(invoice_id)
        if payment:
            user_tg_id = payment.user.telegram_id
            user_lang = payment.user.language
            
            user_alert = {
                "uz_latin": "🎉 <b>Ajoyib xabar!</b> Sizning to'lovingiz tasdiqlandi. <b>{plan}</b> tarifi faollashtirildi! Uni 👤 <b>Profilim</b> menyusida tekshiring.",
                "uz_cyrillic": "🎉 <b>Ажойиб хабар!</b> Сизнинг тўловингиз тасдиқланди. <b>{plan}</b> тарифи фаоллаштирилди! Уни 👤 <b>Профилим</b> менюсида текширинг.",
                "ru": "🎉 <b>Отличная новость!</b> Ваш платеж был подтвержден. Тариф <b>{plan}</b> активирован! Проверьте его статус в меню 👤 <b>Мой профиль</b>."
            }
            
            try:
                await bot.send_message(
                    chat_id=user_tg_id,
                    text=user_alert.get(user_lang, user_alert["uz_latin"]).format(plan=payment.plan.name_uz if user_lang != "ru" else payment.plan.name_ru)
                )
            except Exception as notify_err:
                logger.error(f"Foydalanuvchini to'lov haqida xabardor qilishda xatolik: {notify_err}")

        await callback.answer("To'lov muvaffaqiyatli tasdiqlandi", show_alert=True)
        await callback.message.delete()
    else:
        await callback.answer(f"Xatolik: {message}", show_alert=True)

@router.callback_query(F.data.startswith("admin_reject_pay_"))
async def callback_admin_reject_payment(callback: CallbackQuery, payment_repo: PaymentRepository, audit_repo: AuditRepository, current_user: Any):
    """Admin to'lovni rad etganda"""
    if current_user.telegram_id not in settings.ADMIN_IDS and current_user.role not in ["admin", "superadmin"]:
        return

    invoice_id = callback.data.replace("admin_reject_pay_", "")
    
    payment = await payment_repo.get_by_invoice_id(invoice_id)
    if payment:
        await payment_repo.mark_as_failed(payment.id, raw_payload={"rejected_by": current_user.telegram_id})
        
        # Audit log
        await audit_repo.log_action(
            admin_id=current_user.telegram_id,
            action="manual_reject_payment",
            entity_type="payment",
            entity_id=payment.id,
            old_value_json={"status": "pending"},
            new_value_json={"status": "failed"}
        )
        
        await callback.answer("To'lov rad etildi va o'chirildi", show_alert=True)
        await callback.message.delete()
    else:
        await callback.answer("To'lov topilmadi", show_alert=True)
