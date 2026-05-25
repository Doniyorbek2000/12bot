import logging
from typing import Any
from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from app.bot.states.user_states import UserStates
from app.bot.keyboards.user_keyboards import get_back_keyboard, get_main_menu, get_cancel_inline
from app.utils.texts import TEXTS
from app.services.gemini_service import GeminiService
from app.services.legal_ai_service import LegalAIService
from app.services.usage_service import UsageService
from app.db.repositories.question_repo import QuestionRepository
from app.db.repositories.plan_repo import PlanRepository

logger = logging.getLogger("adolat_ai_bot.legal_question_handler")
router = Router(name="legal_question")

# Initialize services dynamically
gemini_service = GeminiService()
legal_ai = LegalAIService(gemini_service)

@router.message(F.text.in_([TEXTS["buttons"]["ask_question"]["uz_latin"], TEXTS["buttons"]["ask_question"]["uz_cyrillic"], TEXTS["buttons"]["ask_question"]["ru"]]))
async def ask_question_start(message: Message, state: FSMContext, current_user: Any):
    """Huquqiy savol berish bo'limi bosilganda"""
    lang = current_user.language
    await state.set_state(UserStates.asking_legal_question)
    
    await message.answer(
        text=TEXTS["ask_question_prompt"][lang],
        reply_markup=get_back_keyboard(lang)
    )

@router.message(UserStates.asking_legal_question)
async def process_legal_question(message: Message, state: FSMContext, current_user: Any, question_repo: QuestionRepository, plan_repo: PlanRepository):
    """Foydalanuvchi huquqiy savol yozib yuborganda ishlaydi"""
    lang = current_user.language
    question_text = message.text.strip()
    
    # Orqaga yoki Bosh menyu tugmasini tekshirish
    if question_text in [TEXTS["buttons"]["back"][lang], TEXTS["buttons"]["main_menu"][lang]]:
        await state.clear()
        await message.answer(
            text=TEXTS["main_menu_text"][lang],
            reply_markup=get_main_menu(lang)
        )
        return

    # 1. Limit tekshirish
    usage_service = UsageService(user_repo=None, plan_repo=plan_repo)
    # user_repo middleware-dan kelgan session bilan bog'langan
    from app.db.repositories.user_repo import UserRepository
    usage_service.user_repo = UserRepository(question_repo.db)
    
    can_ask, err_msg = await usage_service.can_ask_question(current_user.telegram_id)
    if not can_ask:
        await state.clear()
        
        # Limit tugagani haqida ogohlantirish va tariflar bo'limini taklif qilish
        tariffs_prompt = {
            "uz_latin": "\n\nLimitni yangilash yoki oshirish uchun 💳 <b>Tariflar va to'lov</b> menyusidan yangi tarif sotib oling.",
            "uz_cyrillic": "\n\nЛимитни янгилаш ёки ошириш учун 💳 <b>Тарифлар ва тўлов</b> менюсидан янги тариф сотиб олинг.",
            "ru": "\n\nДля продления или увеличения лимита приобретите тариф в меню 💳 <b>Тарифы и оплата</b>."
        }
        await message.answer(
            text=f"⚠️ {err_msg}{tariffs_prompt[lang]}",
            reply_markup=get_main_menu(lang)
        )
        return

    # 2. Loading xabarini yuborish
    loading_messages = {
        "uz_latin": "⏳ <i>Savolingiz tahlil qilinmoqda...\n⚖️ Huquqiy javob tayyorlanmoqda...</i>",
        "uz_cyrillic": "⏳ <i>Саволингиз таҳлил қилинмоқда...\n⚖️ Ҳуқуқий жавоб тайёрланмоқда...</i>",
        "ru": "⏳ <i>Ваш вопрос анализируется...\n⚖️ Готовится юридический ответ...</i>"
    }
    loading_msg = await message.answer(text=loading_messages[lang])

    try:
        # 3. Gemini API ga yuborish
        logger.info(f"Foydalanuvchi ID {current_user.telegram_id} savoli Gemini ga yuborilmoqda.")
        ai_res = await legal_ai.answer_legal_question(question_text, lang)
        
        # 4. Javobni foydalanuvchiga yuborish (juda uzun bo'lsa bo'lib yuborish)
        full_reply = ai_res["text"]
        
        # Telegram 4096 belgi limitini hisobga olgan holda bo'lib yuboramiz
        if len(full_reply) > 4000:
            chunks = [full_reply[i:i+4000] for i in range(0, len(full_reply), 4000)]
            for chunk in chunks:
                await message.answer(text=chunk)
        else:
            await message.answer(text=full_reply)

        # 5. Savol va javobni tarixda saqlash
        await question_repo.create_question(
            user_id=current_user.id,
            question_text=question_text,
            answer_text=full_reply,
            language=lang,
            model_name=ai_res["model"],
            tokens_input=ai_res["input_tokens"],
            tokens_output=ai_res["output_tokens"],
            status=ai_res["status"]
        )
        
    except Exception as e:
        logger.error(f"Huquqiy savolga javob tayyorlashda xatolik: {e}")
        error_msg = {
            "uz_latin": "❌ Kechirasiz, javob tayyorlashda xatolik yuz berdi. Iltimos birozdan so'ng qayta urinib ko'ring.",
            "uz_cyrillic": "❌ Кечирасиз, жавоб тайёрлашда хатолик юз берди. Илтимос бироздан сўнг қайта уриниб кўринг.",
            "ru": "❌ Извините, произошла ошибка при подготовке ответа. Пожалуйста, попробуйте позже."
        }
        await message.answer(text=error_msg[lang])
        
    finally:
        # Loading xabarini o'chirish
        await loading_msg.delete()
        # State-ni tozalash
        await state.clear()
        # Asosiy menyu
        await message.answer(
            text=TEXTS["main_menu_text"][lang],
            reply_markup=get_main_menu(lang)
        )
