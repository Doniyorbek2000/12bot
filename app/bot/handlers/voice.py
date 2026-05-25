import os
import logging
from typing import Any
from aiogram import Router, F, Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from app.bot.states.user_states import UserStates
from app.bot.keyboards.user_keyboards import get_back_keyboard, get_main_menu
from app.utils.texts import TEXTS
from app.services.gemini_service import GeminiService
from app.services.legal_ai_service import LegalAIService
from app.services.usage_service import UsageService
from app.services.voice_service import VoiceService
from app.db.repositories.question_repo import QuestionRepository
from app.db.repositories.plan_repo import PlanRepository

logger = logging.getLogger("adolat_ai_bot.voice_handler")
router = Router(name="voice")

# Initialize services
gemini_service = GeminiService()
legal_ai = LegalAIService(gemini_service)
voice_service = VoiceService()

@router.message(F.text.in_([TEXTS["buttons"]["voice_question"]["uz_latin"], TEXTS["buttons"]["voice_question"]["uz_cyrillic"], TEXTS["buttons"]["voice_question"]["ru"]]))
async def voice_start(message: Message, state: FSMContext, current_user: Any):
    """Ovozli savol berish bo'limi bosilganda"""
    lang = current_user.language
    await state.set_state(UserStates.sending_voice)
    
    await message.answer(
        text=TEXTS["voice_prompt"][lang],
        reply_markup=get_back_keyboard(lang)
    )

@router.message(UserStates.sending_voice, F.voice)
async def process_voice_message(message: Message, state: FSMContext, bot: Bot, current_user: Any, question_repo: QuestionRepository, plan_repo: PlanRepository):
    """Foydalanuvchi ovozli xabar yuborganda ishlaydi"""
    lang = current_user.language
    voice = message.voice
    
    # 1. Limit va Tarifni tekshirish
    from app.db.repositories.user_repo import UserRepository
    usage_service = UsageService(user_repo=UserRepository(question_repo.db), plan_repo=plan_repo)
    can_use, err_msg = await usage_service.can_use_voice(current_user.telegram_id, voice.duration)
    if not can_use:
        await state.clear()
        await message.answer(
            text=f"⚠️ {err_msg}",
            reply_markup=get_main_menu(lang)
        )
        return

    # 2. Loading xabarini yuborish
    loading_messages = {
        "uz_latin": "🎙 <i>Ovozli xabar yuklab olinmoqda va matnga aylantirilmoqda...\n⏳ Iltimos kuting...</i>",
        "uz_cyrillic": "🎙 <i>Овозли хабар юклаб олинмоқда ва матнга айлантирилмоқда...\n⏳ Илтимос кутинг...</i>",
        "ru": "🎙 <i>Голосовое сообщение скачивается и расшифровывается...\n⏳ Пожалуйста, подождите...</i>"
    }
    loading_msg = await message.answer(text=loading_messages[lang])

    try:
        # Ovozli faylni vaqtinchalik saqlash joyi
        voice_file_path = f"generated_docs/voice_{message.from_user.id}_{voice.file_id[:8]}.ogg"
        
        # 3. Faylni yuklab olish
        file_info = await bot.get_file(voice.file_id)
        await bot.download_file(file_info.file_path, voice_file_path)

        # 4. Speech-to-Text (Ovozni matnga o'tkazish)
        extracted_question = await voice_service.speech_to_text(voice_file_path)
        
        # Foydalanuvchiga ovozdan nima ajratib olinganini ko'rsatamiz
        stt_info = {
            "uz_latin": f"🎙 <b>Sizning savolingiz:</b>\n<i>\"{extracted_question}\"</i>\n\n⚖️ <b>Huquqiy javob tayyorlanmoqda...</b>",
            "uz_cyrillic": f"🎙 <b>Сизнинг саволингиз:</b>\n<i>\"{extracted_question}\"</i>\n\n⚖️ <b>Ҳуқуқий жавоб тайёрланмоқда...</b>",
            "ru": f"🎙 <b>Ваш вопрос:</b>\n<i>«{extracted_question}»</i>\n\n⚖️ <b>Готовится юридический ответ...</b>"
        }
        await loading_msg.edit_text(text=stt_info[lang])

        # 5. Gemini API dan huquqiy javob olish
        ai_res = await legal_ai.answer_legal_question(extracted_question, lang)
        answer_text = ai_res["text"]

        # 6. Javobni foydalanuvchiga yuborish
        if len(answer_text) > 4000:
            chunks = [answer_text[i:i+4000] for i in range(0, len(answer_text), 4000)]
            for chunk in chunks:
                await message.answer(text=chunk)
        else:
            await message.answer(text=answer_text)

        # 7. Savolni bazada saqlash
        await question_repo.create_question(
            user_id=current_user.id,
            question_text=f"[Ovozli so'rov]: {extracted_question}",
            answer_text=answer_text,
            language=lang,
            model_name=ai_res["model"],
            tokens_input=ai_res["input_tokens"],
            tokens_output=ai_res["output_tokens"],
            status=ai_res["status"]
        )

        # Vaqtinchalik faylni o'chirish
        if os.path.exists(voice_file_path):
            os.remove(voice_file_path)

    except Exception as e:
        logger.error(f"Ovozli savolni qayta ishlashda xatolik: {e}")
        error_msg = {
            "uz_latin": "❌ Ovozli savolni qayta ishlashda xatolik yuz berdi. Iltimos birozdan so'ng qayta urinib ko'ring.",
            "uz_cyrillic": "❌ Овозли саволни қайта ишлашда хатолик юз берди. Илтимос қайтадан уриниб кўринг.",
            "ru": "❌ Произошла ошибка при обработке голосового сообщения. Пожалуйста, попробуйте еще раз."
        }
        await message.answer(text=error_msg[lang])
        
    finally:
        # Loading xabarini o'chirish
        try:
            await loading_msg.delete()
        except Exception:
            pass
        # State tozalash
        await state.clear()
        # Bosh menyu
        await message.answer(
            text=TEXTS["main_menu_text"][lang],
            reply_markup=get_main_menu(lang)
        )
