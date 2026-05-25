import logging
from typing import Any
from aiogram import Router, F
from aiogram.types import Message
from app.utils.texts import TEXTS
from app.services.usage_service import UsageService
from app.db.repositories.plan_repo import PlanRepository

logger = logging.getLogger("adolat_ai_bot.profile_handler")
router = Router(name="profile")

@router.message(F.text.in_([TEXTS["buttons"]["profile"]["uz_latin"], TEXTS["buttons"]["profile"]["uz_cyrillic"], TEXTS["buttons"]["profile"]["ru"]]))
async def view_profile(message: Message, current_user: Any, plan_repo: PlanRepository):
    """Foydalanuvchi profil ma'lumotlarini ko'rish"""
    lang = current_user.language
    
    # Usage service yordamida yangi limit ma'lumotlarini tekshirish va olish
    from app.db.repositories.user_repo import UserRepository
    usage_service = UsageService(user_repo=UserRepository(plan_repo.db), plan_repo=plan_repo)
    user, plan, counter = await usage_service.get_or_check_user_limits(current_user.telegram_id)

    # Qolgan limitlarni hisoblash
    questions_left = max(0, plan.question_limit - counter.questions_used)
    analysis_left = max(0, plan.document_analysis_limit - counter.document_analysis_used)
    generation_left = max(0, plan.document_generation_limit - counter.document_generation_used)
    voice_left = max(0.0, plan.voice_limit_minutes - counter.voice_minutes_used)

    # Tarif tugash sanasini chiroyli formatlash
    plan_expiry = user.plan_expires_at.strftime("%d.%m.%Y") if user.plan_expires_at else "Cheksiz"
    reg_date = user.created_at.strftime("%d.%m.%Y")

    plan_name = plan.name_uz if lang != "ru" else plan.name_ru

    # Ko'p tilli profil matnlari
    profile_texts = {
        "uz_latin": (
            "👤 <b>Sizning Shaxsiy Profilingiz</b>\n\n"
            "🆔 <b>Telegram ID:</b> <code>{tg_id}</code>\n"
            "✍️ <b>Ism:</b> {name}\n"
            "🌐 <b>Tizim tili:</b> {lang_name}\n"
            "📅 <b>Ro'yxatdan o'tgan sana:</b> {reg_date}\n\n"
            "💳 <b>Joriy Tarif:</b> <b>{plan_name}</b>\n"
            "⌛ <b>Tarif tugash sanasi:</b> <code>{plan_expiry}</code>\n\n"
            "📊 <b>Qolgan limitlaringiz (Ushbu davr uchun):</b>\n"
            "• ⚖️ Huquqiy savollar: <code>{q_left} ta</code> (Jami: {q_total} ta)\n"
            "• 📄 Hujjat tahlillari: <code>{a_left} ta</code> (Jami: {a_total} ta)\n"
            "• 📝 Hujjat yaratish: <code>{g_left} ta</code> (Jami: {g_total} ta)\n"
            "• 🎙 Ovozli so'rovlar: <code>{v_left:.1f} daqiqa</code> (Jami: {v_total} daq)\n"
        ),
        "uz_cyrillic": (
            "👤 <b>Сизнинг Шахсий Профилингиз</b>\n\n"
            "🆔 <b>Telegram ID:</b> <code>{tg_id}</code>\n"
            "✍️ <b>Исм:</b> {name}\n"
            "🌐 <b>Тизим тили:</b> {lang_name}\n"
            "📅 <b>Рўйхатдан ўтган сана:</b> {reg_date}\n\n"
            "💳 <b>Жорий Тариф:</b> <b>{plan_name}</b>\n"
            "⌛ <b>Тариф тугаш санаси:</b> <code>{plan_expiry}</code>\n\n"
            "📊 <b>Қолган лимитларингиз (Ушбу давр учун):</b>\n"
            "• ⚖️ Ҳуқуқий саволлар: <code>{q_left} та</code> (Жами: {q_total} та)\n"
            "• 📄 Ҳужжат таҳлиллари: <code>{a_left} та</code> (Жами: {a_total} та)\n"
            "• 📝 Ҳужжат яратиш: <code>{g_left} та</code> (Жами: {g_total} та)\n"
            "• 🎙 Овозли сўровлар: <code>{v_left:.1f} дақиқа</code> (Жами: {v_total} дақ)\n"
        ),
        "ru": (
            "👤 <b>Ваш личный профиль</b>\n\n"
            "🆔 <b>Telegram ID:</b> <code>{tg_id}</code>\n"
            "✍️ <b>Имя:</b> {name}\n"
            "🌐 <b>Язык системы:</b> {lang_name}\n"
            "📅 <b>Дата регистрации:</b> {reg_date}\n\n"
            "💳 <b>Текущий тариф:</b> <b>{plan_name}</b>\n"
            "⌛ <b>Дата окончания тарифа:</b> <code>{plan_expiry}</code>\n\n"
            "📊 <b>Оставшиеся лимиты (на текущий период):</b>\n"
            "• ⚖️ Юридические вопросы: <code>{q_left} шт</code> (Всего: {q_total})\n"
            "• 📄 Анализ документов: <code>{a_left} шт</code> (Всего: {a_total})\n"
            "• 📝 Создание документов: <code>{g_left} шт</code> (Всего: {g_total})\n"
            "• 🎙 Голосовые запросы: <code>{v_left:.1f} минут</code> (Всего: {v_total} мин)\n"
        )
    }

    langs_names = {
        "uz_latin": "🇺🇿 O'zbekcha",
        "uz_cyrillic": "🇺🇿 Ўзбекча",
        "ru": "🇷🇺 Русский"
    }

    formatted_text = profile_texts.get(lang, profile_texts["uz_latin"]).format(
        tg_id=user.telegram_id,
        name=user.first_name,
        lang_name=langs_names.get(lang, "O'zbekcha"),
        reg_date=reg_date,
        plan_name=plan_name,
        plan_expiry=plan_expiry,
        q_left=questions_left, q_total=plan.question_limit,
        a_left=analysis_left, a_total=plan.document_analysis_limit,
        g_left=generation_left, g_total=plan.document_generation_limit,
        v_left=voice_left, v_total=plan.voice_limit_minutes
    )

    await message.answer(text=formatted_text)
