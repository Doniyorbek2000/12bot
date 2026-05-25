import logging
from typing import Any, List, Dict
from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile
from aiogram.fsm.context import FSMContext
from app.bot.states.user_states import UserStates
from app.bot.keyboards.user_keyboards import get_back_keyboard, get_main_menu, get_cancel_inline
from app.utils.texts import TEXTS
from app.services.gemini_service import GeminiService
from app.services.legal_ai_service import LegalAIService
from app.services.usage_service import UsageService
from app.services.document_generator import DocumentGenerator
from app.db.repositories.document_repo import DocumentRepository
from app.db.repositories.plan_repo import PlanRepository

logger = logging.getLogger("adolat_ai_bot.document_generation_handler")
router = Router(name="document_generation")

# Initialize services
gemini_service = GeminiService()
legal_ai = LegalAIService(gemini_service)
doc_generator = DocumentGenerator()

# Dynamic Hujjat yaratish savollar ro'yxati
QUESTIONS = [
    {"key": "receiver", "uz": "🏢 Hujjat kimga yuboriladi? (Masalan: 'Yashnobod tuman sudi raisiga' yoki 'MIB Toshkent shahar boshqarmasiga')", "ru": "🏢 Кому направляется документ? (Например: 'Председателю Яшнабадского районного суда' или 'В БПИ города Ташкента')"},
    {"key": "sender", "uz": "👤 Hujjat kimdan? F.I.Sh., yashash manzilingiz va telefon raqamingizni yozing. (Masalan: 'Toshkent sh., Chilonzor 4-daha, 12-uy, 45-xonadonda yashovchi Karimov Anvar, tel: +998901234567')", "ru": "👤 От кого документ? Укажите Ф.И.О., адрес проживания и телефон. (Например: 'Каримов Анвар, проживающий по адресу г. Ташкент, Чиланзар 4, д. 12, кв. 45, тел: +998901234567')"},
    {"key": "description", "uz": "📝 Holat tavsifi. Muammoingizni qisqacha yozing. (Masalan: 'Qarzdor Aliyev Davron mendan 2025-yil 1-oktyabrda tilxat asosida 10 000 000 so'm pul olib, muddati kelganda ham qaytarmayapti')", "ru": "📝 Описание ситуации. Кратко опишите вашу проблему. (Например: 'Должник Алиев Даврон взял у меня 10 000 000 сумов под расписку 1 октября 2025 года и не возвращает в срок')"},
    {"key": "demand", "uz": "💡 Sizning talabingiz yoki iltimosingiz. Nima hal qilinishini xohlaysiz? (Masalan: 'Qarzdorlikni va sud xarajatlarini undirib berishingizni so'rayman')", "ru": "💡 Ваше требование или просьба. Что именно вы просите решить? (Например: 'Прошу взыскать сумму долга и судебные расходы')"},
    {"key": "additional", "uz": "➕ Qo'shimcha izohlar yoki ilovalar bormi? (Masalan: 'Tilxat nusxasi mavjud' yoki 'Yo'q')", "ru": "➕ Есть ли дополнительные примечания или приложения? (Например: 'Копия расписки прилагается' или 'Нет')"}
]

def get_doc_types_keyboard(lang: str = "uz_latin") -> InlineKeyboardMarkup:
    """Hujjat turlarini tanlash inline klaviaturasi"""
    btn_text = {
        "uz_latin": {
            "ariza": "📝 Ariza", "shikoyat": "📢 Shikoyat", "da'vo": "⚖️ Da'vo ariza",
            "tushuntirish": "📋 Tushuntirish xati", "murojaat": "✉️ Murojaat", "mehnat": "💼 Mehnat bo'yicha shikoyat",
            "aliment": "👶 Aliment bo'yicha ariza", "qarz": "💰 Qarz talabnomasi", "erkin": "✍️ Erkin yuridik hujjat"
        },
        "uz_cyrillic": {
            "ariza": "📝 Ариза", "shikoyat": "📢 Шикоят", "da'vo": "⚖️ Даъво ариза",
            "tushuntirish": "📋 Тушунтириш хати", "murojaat": "✉️ Мурожаат", "mehnat": "💼 Меҳнат бўйича шикоят",
            "aliment": "👶 Алимент бўйича ариза", "qarz": "💰 Қарз талабномаси", "erkin": "✍️ Эркин юридик ҳужжат"
        },
        "ru": {
            "ariza": "📝 Заявление", "shikoyat": "📢 Жалоба", "da'vo": "⚖️ Исковое заявление",
            "tushuntirish": "📋 Объяснительная", "murojaat": "✉️ Обращение", "mehnat": "💼 Жалоба по трудовым спорам",
            "aliment": "👶 Заявление на алименты", "qarz": "💰 Требование о долге", "erkin": "✍️ Свободный юр. документ"
        }
    }
    
    t = btn_text.get(lang, btn_text["uz_latin"])
    
    keyboard = [
        [InlineKeyboardButton(text=t["ariza"], callback_data="gen_doc_ariza"), InlineKeyboardButton(text=t["shikoyat"], callback_data="gen_doc_shikoyat")],
        [InlineKeyboardButton(text=t["da'vo"], callback_data="gen_doc_da'vo_ariza"), InlineKeyboardButton(text=t["tushuntirish"], callback_data="gen_doc_tushuntirish_xati")],
        [InlineKeyboardButton(text=t["murojaat"], callback_data="gen_doc_murojaat"), InlineKeyboardButton(text=t["mehnat"], callback_data="gen_doc_mehnat_shikoyati")],
        [InlineKeyboardButton(text=t["aliment"], callback_data="gen_doc_aliment_ariza"), InlineKeyboardButton(text=t["qarz"], callback_data="gen_doc_qarz_talabnomasi")],
        [InlineKeyboardButton(text=t["erkin"], callback_data="gen_doc_erkin_hujjat")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

@router.message(F.text.in_([TEXTS["buttons"]["doc_generation"]["uz_latin"], TEXTS["buttons"]["doc_generation"]["uz_cyrillic"], TEXTS["buttons"]["doc_generation"]["ru"]]))
async def doc_generation_start(message: Message, state: FSMContext, current_user: Any):
    """Hujjat yaratish bo'limi bosilganda"""
    lang = current_user.language
    await state.set_state(UserStates.choosing_doc_type)
    
    prompt = {
        "uz_latin": "📝 <b>Hujjat tayyorlash bo'limi</b>\n\nTizim sizga rasmiy ariza, shikoyat yoki da'vo arizalarini to'ldirishga yordam beradi. Iltimos, quyidagi ro'yxatdan o'zingizga kerakli hujjat turini tanlang:",
        "uz_cyrillic": "📝 <b>Ҳужжат тайёрлаш бўлими</b>\n\nТизим сизга расмий ариза, шикоят ёки даъво аризаларини тўлдиришга ёрдам беради. Илтимос, қуйидаги рўйхатдан ўзингизга керакли ҳужжат турини танланг:",
        "ru": "📝 <b>Раздел подготовки документов</b>\n\nСистема поможет вам составить официальное заявление, жалобу или иск. Пожалуйста, выберите нужный тип документа из списка ниже:"
    }
    
    await message.answer(
        text=prompt[lang],
        reply_markup=get_doc_types_keyboard(lang)
    )

@router.callback_query(UserStates.choosing_doc_type, F.data.startswith("gen_doc_"))
async def callback_choose_doc_type(callback: CallbackQuery, state: FSMContext, current_user: Any, plan_repo: PlanRepository):
    """Foydalanuvchi hujjat turini tanlaganda ishlaydi"""
    doc_type = callback.data.replace("gen_doc_", "")
    lang = current_user.language
    
    # 1. Limit tekshirish
    from app.db.repositories.user_repo import UserRepository
    usage_service = UsageService(user_repo=UserRepository(plan_repo.db), plan_repo=plan_repo)
    can_gen, err_msg = await usage_service.can_generate_document(current_user.telegram_id)
    if not can_gen:
        await state.clear()
        await callback.answer(err_msg, show_alert=True)
        await callback.message.delete()
        await callback.message.answer(text=f"⚠️ {err_msg}", reply_markup=get_main_menu(lang))
        return

    # FSM ma'lumotlarini saqlash
    await state.update_data(doc_type=doc_type, current_question_index=0, answers={})
    
    # Birinchi savolni so'rash
    first_q = QUESTIONS[0]
    prompt_text = first_q["uz"] if lang != "ru" else first_q["ru"]
    
    await callback.answer()
    await callback.message.delete()
    
    await state.set_state(UserStates.entering_doc_details)
    await callback.message.answer(
        text=f"<b>1/5-savol:</b>\n\n{prompt_text}",
        reply_markup=get_back_keyboard(lang)
    )

@router.message(UserStates.entering_doc_details)
async def process_doc_details_flow(message: Message, state: FSMContext, current_user: Any, document_repo: DocumentRepository, plan_repo: PlanRepository):
    """Form-Flow: Bosqichma-bosqich savollarga javob yig'ish"""
    lang = current_user.language
    user_text = message.text.strip()
    
    # Orqaga yoki bosh menyuni tekshirish
    if user_text in [TEXTS["buttons"]["back"][lang], TEXTS["buttons"]["main_menu"][lang]]:
        await state.clear()
        await message.answer(
            text=TEXTS["main_menu_text"][lang],
            reply_markup=get_main_menu(lang)
        )
        return

    data = await state.get_data()
    q_idx = data["current_question_index"]
    answers = data["answers"]
    doc_type = data["doc_type"]
    
    # Joriy savol kalitiga javobni saqlash
    current_q_key = QUESTIONS[q_idx]["key"]
    answers[current_q_key] = user_text
    
    # Keyingi savolga o'tish
    next_q_idx = q_idx + 1
    await state.update_data(answers=answers, current_question_index=next_q_idx)

    # Agar barcha savollar to'ldirilgan bo'lsa (5 tadan keyin)
    if next_q_idx >= len(QUESTIONS):
        await state.clear()
        
        # Hujjat yaratish uchun oxirgi marta limitni decrement qilamiz
        from app.db.repositories.user_repo import UserRepository
        usage_service = UsageService(user_repo=UserRepository(document_repo.db), plan_repo=plan_repo)
        can_gen, err_msg = await usage_service.can_generate_document(current_user.telegram_id)
        if not can_gen:
            await message.answer(text=f"⚠️ {err_msg}", reply_markup=get_main_menu(lang))
            return
        
        loading_messages = {
            "uz_latin": "⏳ <i>Hujjat matni tayyorlanmoqda...\n⚖️ O'zbekiston qonunlari bo'yicha huquqiy asoslar shakllantirilmoqda...</i>",
            "uz_cyrillic": "⏳ <i>Ҳужжат матни тайёрланмоқда...\n⚖️ Ўзбекистон қонунлари бўйича ҳуқуқий асослар шакллантирилмоқда...</i>",
            "ru": "⏳ <i>Формируется текст документа...\n⚖️ Подбираются юридические основания законодательства Узбекистана...</i>"
        }
        loading_msg = await message.answer(text=loading_messages[lang])
        
        try:
            # 1. Gemini orqali hujjat matnini generatsiya qilish
            logger.info(f"Foydalanuvchi ID {current_user.telegram_id} uchun {doc_type} hujjati AI tomonidan yaratilmoqda.")
            ai_res = await legal_ai.generate_document(doc_type, answers, lang)
            generated_text = ai_res["text"]
            
            # 2. Word (DOCX) faylini yaratish
            docx_path = doc_generator.create_docx(doc_type, generated_text)
            
            # 3. Bazaga saqlash
            await document_repo.create_generated_document(
                user_id=current_user.id,
                document_type=doc_type,
                input_data_json=answers,
                generated_text=generated_text,
                docx_path=docx_path,
                status="generated"
            )

            # 4. Foydalanuvchiga matnni Telegramda ko'rsatish
            success_msg = {
                "uz_latin": "✅ <b>Hujjatingiz muvaffaqiyatli tayyorlandi!</b>\n\nQuyida hujjat matni va yuklab olish uchun Word (DOCX) formati taqdim etiladi. Uni ochib, [ ] qavs ichidagi ma'lumotlarni o'zingiz tekshiring va imzolang:",
                "uz_cyrillic": "✅ <b>Ҳужжатингиз муваффақиятли тайёрланди!</b>\n\nҚуйида ҳужжат матни ва юклаб олиш учун Word (DOCX) формати тақдим этилади. Уни очиб, [ ] қавс ичидаги маълумотларни ўзингиз текширинг ва имзоланг:",
                "ru": "✅ <b>Ваш документ успешно подготовлен!</b>\n\nНиже предоставлен текст документа и формат Word (DOCX) для скачивания. Откройте его, проверьте данные внутри квадратных скобок [ ] и подпишите:"
            }
            await message.answer(text=success_msg[lang])
            
            # Telegram xabar limiti
            if len(generated_text) > 4000:
                chunks = [generated_text[i:i+4000] for i in range(0, len(generated_text), 4000)]
                for chunk in chunks:
                    await message.answer(text=chunk)
            else:
                await message.answer(text=generated_text)
            
            # 5. DOCX Faylni yuborish
            docx_file = FSInputFile(docx_path, filename=f"Adolat_AI_{doc_type}.docx")
            await message.answer_document(
                document=docx_file,
                caption={
                    "uz_latin": "📝 Tayyor hujjat (Word formati)",
                    "uz_cyrillic": "📝 Тайёр ҳужжат (Word формати)",
                    "ru": "📝 Готовый документ (Формат Word)"
                }[lang]
            )
            
        except Exception as e:
            logger.error(f"Hujjat yaratishda xatolik: {e}")
            await message.answer(
                text={
                    "uz_latin": "❌ Hujjat yaratishda xatolik yuz berdi. Iltimos qaytadan urinib ko'ring.",
                    "uz_cyrillic": "❌ Ҳужжат яратишда хатолик юз берди. Илтимос қайтадан уриниб кўринг.",
                    "ru": "❌ Произошла ошибка при генерации документа. Пожалуйста, попробуйте еще раз."
                }[lang]
            )
        finally:
            await loading_msg.delete()
            # Bosh menyu
            await message.answer(
                text=TEXTS["main_menu_text"][lang],
                reply_markup=get_main_menu(lang)
            )
            
    else:
        # Keyingi savolni berish
        next_q = QUESTIONS[next_q_idx]
        prompt_text = next_q["uz"] if lang != "ru" else next_q["ru"]
        
        await message.answer(
            text=f"<b>{next_q_idx + 1}/5-savol:</b>\n\n{prompt_text}",
            reply_markup=get_back_keyboard(lang)
        )
