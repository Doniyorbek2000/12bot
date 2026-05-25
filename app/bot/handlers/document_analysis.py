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
from app.services.document_reader import DocumentReader
from app.db.repositories.document_repo import DocumentRepository
from app.db.repositories.plan_repo import PlanRepository
from app.db.repositories.user_repo import UserRepository

logger = logging.getLogger("adolat_ai_bot.document_analysis_handler")
router = Router(name="document_analysis")

# Initialize services
gemini_service = GeminiService()
legal_ai = LegalAIService(gemini_service)
doc_reader = DocumentReader()

@router.message(F.text.in_([TEXTS["buttons"]["doc_analysis"]["uz_latin"], TEXTS["buttons"]["doc_analysis"]["uz_cyrillic"], TEXTS["buttons"]["doc_analysis"]["ru"]]))
async def doc_analysis_start(message: Message, state: FSMContext, current_user: Any):
    """Hujjat tahlili bo'limi bosilganda"""
    lang = current_user.language
    await state.set_state(UserStates.uploading_document)
    
    await message.answer(
        text=TEXTS["doc_analysis_prompt"][lang],
        reply_markup=get_back_keyboard(lang)
    )

@router.message(UserStates.uploading_document, F.document)
async def process_document_upload(message: Message, state: FSMContext, bot: Bot, current_user: Any, document_repo: DocumentRepository, plan_repo: PlanRepository):
    """Foydalanuvchi hujjat faylini yuborganda ishlaydi"""
    lang = current_user.language
    doc = message.document
    file_name = doc.file_name
    file_size = doc.file_size
    
    # 1. Kengaytmani tekshirish (Whitelist: PDF, DOCX, TXT)
    ext = os.path.splitext(file_name)[1].lower()
    if ext not in [".pdf", ".docx", ".doc", ".txt"]:
        await message.answer(
            text={
                "uz_latin": "❌ Noto'g'ri fayl formati! Faqat <b>PDF, DOCX yoki TXT</b> formatidagi fayllarni yuklang.",
                "uz_cyrillic": "❌ Нотоўғри файл формати! Фақат <b>PDF, DOCX ёки TXT</b> форматидаги файлларни юкланг.",
                "ru": "❌ Неверный формат файла! Загружайте файлы только в форматах <b>PDF, DOCX или TXT</b>."
            }[lang]
        )
        return

    # 2. Limitlarni va fayl hajmini tekshirish
    usage_service = UsageService(user_repo=UserRepository(document_repo.db), plan_repo=plan_repo)
    can_analyze, err_msg = await usage_service.can_analyze_document(current_user.telegram_id, file_size)
    if not can_analyze:
        await state.clear()
        await message.answer(
            text=f"⚠️ {err_msg}",
            reply_markup=get_main_menu(lang)
        )
        return

    # 3. Loading xabarlari
    loading_messages = {
        "uz_latin": "📄 <i>Hujjat yuklab olinmoqda va o'qilmoqda...\n⏳ Sun'iy intellekt tahlili boshlandi, iltimos kuting...</i>",
        "uz_cyrillic": "📄 <i>Ҳужжат юклаб олинмоқда ва ўқилмоқда...\n⏳ Сунъий интеллект таҳлили бошланди, илтимос кутинг...</i>",
        "ru": "📄 <i>Документ скачивается и считывается...\n⏳ Начинается анализ ИИ, пожалуйста подождите...</i>"
    }
    loading_msg = await message.answer(text=loading_messages[lang])

    # Ma'lumotlar bazasida faylni dastlabki ro'yxatga olish
    db_doc = await document_repo.create_uploaded_document(
        user_id=current_user.id,
        telegram_file_id=doc.file_id,
        file_name=file_name,
        file_type=ext.replace(".", ""),
        file_size=file_size
    )

    try:
        # 4. Telegramdan faylni bayt formatida asinxron yuklab olish
        file_info = await bot.get_file(doc.file_id)
        file_io = await bot.download_file(file_info.file_path)
        file_bytes = file_io.read()

        # 5. Fayldan matn ajratish
        extracted_text = doc_reader.read_document(file_bytes, file_name)
        
        # 6. Gemini yordamida tahlil qilish
        logger.info(f"Foydalanuvchi ID {current_user.telegram_id} hujjati Gemini da tahlil qilinmoqda.")
        ai_res = await legal_ai.analyze_document(extracted_text, file_name, lang)
        
        analysis_result = ai_res["text"]

        # 7. Tahlilni foydalanuvchiga yuborish (Belgilar limiti tekshiriladi)
        if len(analysis_result) > 4000:
            chunks = [analysis_result[i:i+4000] for i in range(0, len(analysis_result), 4000)]
            for chunk in chunks:
                await message.answer(text=chunk)
        else:
            await message.answer(text=analysis_result)

        # 8. Bazada natijani yangilash
        await document_repo.update_analysis_result(
            doc_id=db_doc.id,
            extracted_text=extracted_text[:10000], # Birinchi 10k belgini saqlaymiz (baza to'lib ketmasligi uchun)
            analysis_result=analysis_result,
            status="analyzed"
        )

    except Exception as e:
        logger.error(f"Hujjat tahlili jarayonida xatolik: {e}")
        await document_repo.update_analysis_result(
            doc_id=db_doc.id,
            extracted_text="",
            analysis_result=f"Xatolik: {str(e)}",
            status="failed"
        )
        
        error_msg = {
            "uz_latin": "❌ Hujjatni tahlil qilishda xatolik yuz berdi. Fayl matnli formatda ekanligini yoki skaner qilingan rasm emasligini tekshiring.",
            "uz_cyrillic": "❌ Ҳужжатни таҳлил қилишда хатолик юз берди. Файл матнли форматда эканлигини ёки сканер қилинган расм эмаслигини текширинг.",
            "ru": "❌ Произошла ошибка при анализе документа. Убедитесь, что файл содержит текстовый слой и не является сканированным изображением."
        }
        await message.answer(text=error_msg[lang])
        
    finally:
        # Loading xabarini o'chirish
        await loading_msg.delete()
        # State tozalash
        await state.clear()
        # Asosiy menyu
        await message.answer(
            text=TEXTS["main_menu_text"][lang],
            reply_markup=get_main_menu(lang)
        )

@router.message(UserStates.uploading_document)
async def process_document_upload_invalid(message: Message, current_user: Any):
    """Foydalanuvchi fayl o'rniga matn yuborganda ishlaydi"""
    lang = current_user.language
    
    # Agar orqaga/bosh menyu tugmalari bosilgan bo'lsa buni start_handler yoki menu_handler ko'rib oladi
    # Lekin shunchaki matn bo'lsa ogohlantirish beramiz
    if message.text in [TEXTS["buttons"]["back"][lang], TEXTS["buttons"]["main_menu"][lang]]:
        return
        
    await message.answer(
        text={
            "uz_latin": "⚠️ Iltimos, tahlil qilish uchun hujjat faylini yuboring (PDF, DOCX yoki TXT).",
            "uz_cyrillic": "⚠️ Илтимос, таҳлил қилиш учун ҳужжат файлини юборинг (PDF, DOCX ёки TXT).",
            "ru": "⚠️ Пожалуйста, отправьте файл документа (PDF, DOCX или TXT) для анализа."
        }[lang]
    )
