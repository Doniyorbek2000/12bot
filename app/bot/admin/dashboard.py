import logging
from datetime import datetime, time
from typing import Any
from aiogram import Router, F
from aiogram.types import Message
from sqlalchemy import select, func, and_
from app.config import settings
from app.db.models import User, Question, Payment, Plan

logger = logging.getLogger("adolat_ai_bot.admin_dashboard")
router = Router(name="admin_dashboard")

@router.message(F.text == "📊 Dashboard")
async def view_admin_dashboard(message: Message, current_user: Any, db_session: Any):
    """Admin dashboard ma'lumotlarini bazadan hisoblab chiqarish"""
    # Xavfsizlik tekshiruvi
    if current_user.telegram_id not in settings.ADMIN_IDS and current_user.role not in ["admin", "superadmin"]:
        return

    # Bugungi kun boshlanishi
    today_start = datetime.combine(datetime.utcnow().date(), time.min)

    try:
        # 1. Jami foydalanuvchilar
        stmt_users = select(func.count(User.id))
        res_users = await db_session.execute(stmt_users)
        total_users = res_users.scalar() or 0

        # 2. Bugungi yangi foydalanuvchilar
        stmt_today_users = select(func.count(User.id)).where(User.created_at >= today_start)
        res_today_users = await db_session.execute(stmt_today_users)
        today_users = res_today_users.scalar() or 0

        # 3. Jami savollar soni
        stmt_questions = select(func.count(Question.id))
        res_questions = await db_session.execute(stmt_questions)
        total_questions = res_questions.scalar() or 0

        # 4. Bugungi savollar soni
        stmt_today_questions = select(func.count(Question.id)).where(Question.created_at >= today_start)
        res_today_questions = await db_session.execute(stmt_today_questions)
        today_questions = res_today_questions.scalar() or 0

        # 5. Jami to'langan to'lovlar summasi va bugungi tushum
        stmt_payments = select(func.sum(Payment.amount)).where(Payment.status == "paid")
        res_payments = await db_session.execute(stmt_payments)
        total_earnings = res_payments.scalar() or 0.0

        # Bugungi tushum
        stmt_today_payments = select(func.sum(Payment.amount)).where(
            and_(Payment.status == "paid", Payment.paid_at >= today_start)
        )
        res_today_payments = await db_session.execute(stmt_today_payments)
        today_earnings = res_today_payments.scalar() or 0.0

        # 6. Gemini tokenlar statistikasi
        stmt_tokens = select(func.sum(Question.tokens_input), func.sum(Question.tokens_output))
        res_tokens = await db_session.execute(stmt_tokens)
        tokens = res_tokens.fetchone()
        tokens_in = tokens[0] or 0 if tokens else 0
        tokens_out = tokens[1] or 0 if tokens else 0

        # 7. Aktiv premium va Free foydalanuvchilar
        # FREE plan id sini aniqlash
        stmt_free = select(Plan.id).where(Plan.code == "FREE")
        res_free = await db_session.execute(stmt_free)
        free_plan_id = res_free.scalar()

        # Free foydalanuvchilar soni
        stmt_free_users = select(func.count(User.id)).where(User.current_plan_id == free_plan_id)
        res_free_users = await db_session.execute(stmt_free_users)
        free_users = res_free_users.scalar() or 0

        premium_users = max(0, total_users - free_users)

        # Matn tuzish
        dashboard_text = (
            "📊 <b>“Adolat AI” Tizim Dashboardi:</b>\n\n"
            "👥 <b>Foydalanuvchilar:</b>\n"
            "• Jami: <code>{total_u} ta</code>\n"
            "• Bugun yangi: <code>{today_u} ta</code>\n"
            "• Premium a'zolar: <code>{prem_u} ta</code>\n"
            "• Free a'zolar: <code>{free_u} ta</code>\n\n"
            "💬 <b>Savollar va AI faolligi:</b>\n"
            "• Jami savol-javoblar: <code>{total_q} ta</code>\n"
            "• Bugungi savollar: <code>{today_q} ta</code>\n\n"
            "💳 <b>Moliyaviy tahlil:</b>\n"
            "• Jami daromad: <b>{total_e:,.0f} so'm</b>\n"
            "• Bugungi tushum: <b>{today_e:,.0f} so'm</b>\n\n"
            "⚙️ <b>Gemini Tokenlar Sarfi:</b>\n"
            "• Kiruvchi (Input): <code>{tokens_in:,} tokens</code>\n"
            "• Chiquvchi (Output): <code>{tokens_out:,} tokens</code>\n"
            "• Jami: <code>{total_tok:,} tokens</code>\n"
        ).format(
            total_u=total_users, today_u=today_users, prem_u=premium_users, free_u=free_users,
            total_q=total_questions, today_q=today_questions,
            total_e=total_earnings, today_e=today_earnings,
            tokens_in=tokens_in, tokens_out=tokens_out, total_tok=(tokens_in + tokens_out)
        )

        await message.answer(text=dashboard_text)

    except Exception as e:
        logger.error(f"Dashboard ma'lumotlarini yuklashda xatolik: {e}")
        await message.answer("❌ Dashboard statistikalarini yuklashda xatolik yuz berdi.")
