import logging
from typing import Any
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from app.utils.texts import TEXTS
from app.db.repositories.question_repo import QuestionRepository
from app.db.repositories.document_repo import DocumentRepository

logger = logging.getLogger("adolat_ai_bot.history_handler")
router = Router(name="history")

@router.message(F.text.in_([TEXTS["buttons"]["history"]["uz_latin"], TEXTS["buttons"]["history"]["uz_cyrillic"], TEXTS["buttons"]["history"]["ru"]]))
async def view_history(message: Message, current_user: Any, question_repo: QuestionRepository, document_repo: DocumentRepository):
    """Foydalanuvchining so'rovlar tarixini ko'rsatish"""
    lang = current_user.language
    
    # 1. Oxirgi savollar
    questions = await question_repo.get_history_by_user(current_user.id, limit=5)
    # 2. Hujjat tahlillari
    uploads = await document_repo.get_uploaded_by_user(current_user.id, limit=5)
    # 3. Generatsiya qilingan hujjatlar
    generations = await document_repo.get_generated_by_user(current_user.id, limit=5)

    history_text = {
        "uz_latin": "📚 <b>Sizning faollik tarixingiz (Oxirgi so'rovlar):</b>\n\n",
        "uz_cyrillic": "📚 <b>Сизнинг фаоллик тарихингиз (Охирги сўровлар):</b>\n\n",
        "ru": "📚  <b>Ваша история активности (Последние запросы):</b>\n\n"
    }[lang]

    # Savollar bo'limi
    history_text += "💬 <b>Huquqiy savollar:</b>\n"
    if not questions:
        history_text += "• <i>Hali savol berilmagan</i>\n"
    for q in questions:
        q_snippet = q.question_text[:40] + "..." if len(q.question_text) > 40 else q.question_text
        history_text += f"• <code>{q.created_at.strftime('%d.%m %H:%M')}</code>: {q_snippet}\n"

    # Hujjat tahlillari bo'limi
    history_text += "\n📄 <b>Hujjat tahlillari:</b>\n"
    if not uploads:
        history_text += "• <i>Hujjat tahlil qilinmagan</i>\n"
    for u in uploads:
        history_text += f"• <code>{u.created_at.strftime('%d.%m %H:%M')}</code>: {u.file_name} ({u.status})\n"

    # Tayyorlangan hujjatlar bo'limi
    history_text += "\n📝 <b>Tayyorlangan hujjatlar:</b>\n"
    if not generations:
        history_text += "• <i>Hujjat tayyorlanmagan</i>\n"
    for g in generations:
        history_text += f"• <code>{g.created_at.strftime('%d.%m %H:%M')}</code>: {g.document_type.upper()} ({g.status})\n"

    # Tarixni tozalash inline tugmasi
    clear_btn_text = {
        "uz_latin": "🗑 Tarixni tozalash",
        "uz_cyrillic": "🗑 Тарихни тозалаш",
        "ru": "🗑 Очистить историю"
    }
    keyboard = [[InlineKeyboardButton(text=clear_btn_text[lang], callback_data="clear_user_history")]]
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)

    await message.answer(text=history_text, reply_markup=markup)

@router.callback_query(F.data == "clear_user_history")
async def callback_clear_history(callback: CallbackQuery, current_user: Any, question_repo: QuestionRepository):
    """Foydalanuvchi tarixni o'chirishni bosganda"""
    lang = current_user.language
    
    # Savollar tarixini o'chiramiz
    await question_repo.clear_history(current_user.id)
    
    await callback.answer(
        text={
            "uz_latin": "Tarix tozalandi",
            "uz_cyrillic": "Тарих тозаланди",
            "ru": "История очищена"
        }[lang]
    )
    await callback.message.delete()
    await callback.message.answer(
        text={
            "uz_latin": "📚 Tarixingiz muvaffaqiyatli tozalandi.",
            "uz_cyrillic": "📚 Тарихингиз муваффақиятли тозаланди.",
            "ru": "📚 Ваша история успешно очищена."
        }[lang]
    )
