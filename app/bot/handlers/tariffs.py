import logging
from typing import Any
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from app.utils.texts import TEXTS
from app.db.repositories.plan_repo import PlanRepository
from app.services.payment_service import PaymentService
from app.db.repositories.payment_repo import PaymentRepository
from app.db.repositories.user_repo import UserRepository

logger = logging.getLogger("adolat_ai_bot.tariffs_handler")
router = Router(name="tariffs")

def get_payment_providers_keyboard(plan_code: str, lang: str = "uz_latin") -> InlineKeyboardMarkup:
    """To'lov provayderini tanlash inline klaviaturasi"""
    btn_text = {
        "uz_latin": {"click": "Click orqali to'lash", "payme": "Payme orqali to'lash", "mock": "Test to'lov (Mock)"},
        "uz_cyrillic": {"click": "Click орқали тўлаш", "payme": "Payme орқали тўлаш", "mock": "Тест тўлов (Mock)"},
        "ru": {"click": "Оплатить через Click", "payme": "Оплатить через Payme", "mock": "Тестовый платеж (Mock)"}
    }
    
    t = btn_text.get(lang, btn_text["uz_latin"])
    
    keyboard = [
        [
            InlineKeyboardButton(text=t["click"], callback_data=f"pay_prov_click_{plan_code}"),
            InlineKeyboardButton(text=t["payme"], callback_data=f"pay_prov_payme_{plan_code}")
        ],
        [
            InlineKeyboardButton(text=t["mock"], callback_data=f"pay_prov_mock_{plan_code}")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

@router.message(F.text.in_([TEXTS["buttons"]["tariffs"]["uz_latin"], TEXTS["buttons"]["tariffs"]["uz_cyrillic"], TEXTS["buttons"]["tariffs"]["ru"]]))
async def view_tariffs(message: Message, current_user: Any, plan_repo: PlanRepository):
    """Barcha faol tariflar ro'yxatini ko'rsatish"""
    lang = current_user.language
    plans = await plan_repo.get_all_active()
    
    await message.answer(
        text={
            "uz_latin": "💳 <b>“Adolat AI” platformasi tariflari</b>\n\nLimitlar joriy davr (30 kun) uchun amal qiladi. Kerakli tarif ostidagi tugmani bosib xarid qilishingiz mumkin:",
            "uz_cyrillic": "💳 <b>“Адолат АI” платформаси тарифлари</b>\n\nЛимитлар жорий давр (30 кун) учун амал қилади. Керакли тариф остидаги тугмани босиб харид қилишингиз мумкин:",
            "ru": "💳  <b>Тарифы платформы «Adolat AI»</b>\n\nЛимиты действительны в течение текущего периода (30 дней). Выберите подходящий тариф для покупки:"
        }[lang]
    )

    for plan in plans:
        if plan.code == "FREE":
            continue # FREE tarifini bu yerda ko'rsatmaymiz (avtomatik beriladi)
            
        plan_name = plan.name_uz if lang != "ru" else plan.name_ru
        
        # Formatlangan narx
        price_str = f"{plan.price:,.0f} so'm".replace(",", " ")
        if lang == "ru":
            price_str = f"{plan.price:,.0f} сум".replace(",", " ")
            
        voice_str = f"{plan.voice_limit_minutes} daqiqa" if plan.voice_limit_minutes > 0 else "Mavjud emas"
        if lang == "ru" and plan.voice_limit_minutes > 0:
            voice_str = f"{plan.voice_limit_minutes} минут"
        elif lang == "ru":
            voice_str = "Недоступно"

        plan_desc = {
            "uz_latin": (
                "💎 <b>Tarif: {name}</b>\n\n"
                "• ⚖️ Huquqiy savollar: <code>{q_lim} ta</code>\n"
                "• 📄 Hujjat tahlillari: <code>{a_lim} ta</code>\n"
                "• 📝 Hujjat yaratish: <code>{g_lim} ta</code>\n"
                "• 🎙 Ovozli savollar: <code>{v_lim}</code>\n"
                "• 📁 Hujjat hajmi: <code>{size} MB gacha</code>\n"
                "• 📅 Davomiyligi: <code>{days} kun</code>\n\n"
                "💰 Narxi: <b>{price}</b>"
            ),
            "uz_cyrillic": (
                "💎 <b>Тариф: {name}</b>\n\n"
                "• ⚖️ Ҳуқуқий саволлар: <code>{q_lim} та</code>\n"
                "• 📄 Ҳужжат таҳлиллари: <code>{a_lim} та</code>\n"
                "• 📝 Ҳужжат яратиш: <code>{g_lim} та</code>\n"
                "• 🎙 Овозли саволлар: <code>{v_lim}</code>\n"
                "• 📁 Ҳужжат ҳажми: <code>{size} МБ гача</code>\n"
                "• 📅 Давомийлиги: <code>{days} кун</code>\n\n"
                "💰 Нархи: <b>{price}</b>"
            ),
            "ru": (
                "💎 <b>Тариф: {name}</b>\n\n"
                "• ⚖️ Юридические вопросы: <code>{q_lim} шт</code>\n"
                "• 📄 Анализ документов: <code>{a_lim} шт</code>\n"
                "• 📝 Создание документов: <code>{g_lim} шт</code>\n"
                "• 🎙 Голосовые вопросы: <code>{v_lim}</code>\n"
                "• 📁 Макс. размер файла: <code>до {size} МБ</code>\n"
                "• 📅 Срок действия: <code>{days} дней</code>\n\n"
                "💰 Стоимость: <b>{price}</b>"
            )
        }

        buy_btn_text = {
            "uz_latin": f"💳 {plan_name} xarid qilish",
            "uz_cyrillic": f"💳 {plan_name} харид қилиш",
            "ru": f"💳 Купить {plan_name}"
        }

        # Keyboard markup for purchase
        keyboard = [[InlineKeyboardButton(text=buy_btn_text[lang], callback_data=f"buy_plan_{plan.code}")]]
        markup = InlineKeyboardMarkup(inline_keyboard=keyboard)

        formatted_desc = plan_desc.get(lang, plan_desc["uz_latin"]).format(
            name=plan_name,
            q_lim=plan.question_limit,
            a_lim=plan.document_analysis_limit,
            g_lim=plan.document_generation_limit,
            v_lim=voice_str,
            size=plan.max_file_size_mb,
            days=plan.duration_days,
            price=price_str
        )

        await message.answer(text=formatted_desc, reply_markup=markup)

@router.callback_query(F.data.startswith("buy_plan_"))
async def callback_buy_plan(callback: CallbackQuery, current_user: Any):
    """Foydalanuvchi 'Sotib olish' tugmasini bosganda"""
    plan_code = callback.data.replace("buy_plan_", "")
    lang = current_user.language
    
    await callback.answer()
    await callback.message.answer(
        text={
            "uz_latin": "💳 Iltimos, to'lov usulini tanlang:",
            "uz_cyrillic": "💳 Илтимос, тўлов усулини танланг:",
            "ru": "💳 Пожалуйста, выберите способ оплаты:"
        }[lang],
        reply_markup=get_payment_providers_keyboard(plan_code, lang)
    )

@router.callback_query(F.data.startswith("pay_prov_"))
async def callback_process_payment_invoice(callback: CallbackQuery, current_user: Any, payment_repo: PaymentRepository, plan_repo: PlanRepository):
    """Provayder va tarif tanlangandan keyin invoice yaratish"""
    lang = current_user.language
    data_parts = callback.data.replace("pay_prov_", "").split("_")
    provider = data_parts[0]  # click, payme, mock
    plan_code = data_parts[1] # ODDIY, PRO, etc.

    # PaymentService initialize qilish
    user_repo = UserRepository(payment_repo.db)
    payment_service = PaymentService(payment_repo, user_repo, plan_repo)
    
    # Invoice yaratish
    payment, pay_url = await payment_service.create_invoice(
        user_id=current_user.id,
        plan_code=plan_code,
        provider=provider
    )

    if not payment:
        await callback.answer("Hisob yaratishda xatolik yuz berdi", show_alert=True)
        return

    await callback.answer()
    await callback.message.delete()

    payment_info = {
        "uz_latin": (
            "🧾 <b>To'lov hisobi (Invoice) yaratildi</b>\n\n"
            "• 💳 Tarif: <b>{plan_code}</b>\n"
            "• 💰 To'lov summasi: <b>{amount:,.0f} so'm</b>\n"
            "• 🔗 Hisob raqami: <code>{invoice_id}</code>\n"
            "• 🌐 To'lov tizimi: <b>{provider}</b>\n\n"
            "<i>To'lovni amalga oshirish uchun quyidagi tugmani bosing. To'lov yakunlangach tarifingiz avtomatik aktivlashadi.</i>"
        ),
        "uz_cyrillic": (
            "🧾 <b>Тўлов ҳисоби (Invoice) яратилди</b>\n\n"
            "• 💳 Тариф: <b>{plan_code}</b>\n"
            "• 💰 Тўлов суммаси: <b>{amount:,.0f} сўм</b>\n"
            "• 🔗 Ҳисоб рақами: <code>{invoice_id}</code>\n"
            "• 🌐 Тўлов тизими: <b>{provider}</b>\n\n"
            "<i>Тўловни амалга ошириш учун қуйидаги тугмани босинг. Тўлов якунлангач тарифингиз автоматик активлашади.</i>"
        ),
        "ru": (
            "🧾 <b>Счет на оплату (Invoice) успешно создан</b>\n\n"
            "• 💳 Тариф: <b>{plan_code}</b>\n"
            "• 💰 Сумма оплаты: <b>{amount:,.0f} сум</b>\n"
            "• 🔗 Номер счета: <code>{invoice_id}</code>\n"
            "• 🌐 Платежная система: <b>{provider}</b>\n\n"
            "<i>Для совершения платежа нажмите на кнопку ниже. После завершения оплаты ваш тариф активируется автоматически.</i>"
        )
    }

    formatted_text = payment_info.get(lang, payment_info["uz_latin"]).format(
        plan_code=plan_code,
        amount=payment.amount,
        invoice_id=payment.invoice_id,
        provider=provider.upper()
    )

    # To'lov tugmasi
    pay_btn_text = {
        "uz_latin": f"💸 {provider.upper()} orqali to'lash",
        "uz_cyrillic": f"💸 {provider.upper()} орқали тўлаш",
        "ru": f"💸 Оплатить через {provider.upper()}"
    }

    if provider == "mock":
        # Mock to'lov uchun to'liq bepul sinov tugmasi
        pay_btn_text = {
            "uz_latin": "💸 Test to'lovni tasdiqlash",
            "uz_cyrillic": "💸 Тест тўловни тасдиқлаш",
            "ru": "💸 Подтвердить тест-платеж"
        }
        keyboard = [[InlineKeyboardButton(text=pay_btn_text[lang], callback_data=f"mock_confirm_{payment.invoice_id}")]]
    else:
        # Real Click/Payme link
        keyboard = [[InlineKeyboardButton(text=pay_btn_text[lang], url=pay_url)]]
        
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    await callback.message.answer(text=formatted_text, reply_markup=markup)

@router.callback_query(F.data.startswith("mock_confirm_"))
async def callback_mock_payment_confirm(callback: CallbackQuery, payment_repo: PaymentRepository, plan_repo: PlanRepository):
    """Mock to'lovni asinxron faollashtirish"""
    invoice_id = callback.data.replace("mock_confirm_", "")
    
    user_repo = UserRepository(payment_repo.db)
    payment_service = PaymentService(payment_repo, user_repo, plan_repo)
    
    # Mock payment processing
    success, message = await payment_service.process_mock_payment(invoice_id)
    
    await callback.answer()
    await callback.message.delete()
    
    if success:
        await callback.message.answer(
            text={
                "uz_latin": "✅ <b>Muvaffaqiyatli!</b> To'lovingiz qabul qilindi. Tarifingiz faollashtirildi! Uni 👤 <b>Profilim</b> bo'limida tekshirishingiz mumkin.",
                "uz_cyrillic": "✅ <b>Муваффақиятли!</b> Тўловингиз қабул қилинди. Тарифингиз фаоллаштирилди! Уни 👤 <b>Профилим</b> бўлимида текширишингиз мумкин.",
                "ru": "✅  <b>Успешно!</b> Ваш платеж подтвержден. Тариф активирован! Проверить его статус можно в меню 👤 <b>Мой профиль</b>."
            }[callback.from_user.language or "uz_latin"],
            reply_markup=get_main_menu(callback.from_user.language or "uz_latin")
        )
    else:
        await callback.message.answer(
            text=f"❌ Xatolik yuz berdi: {message}",
            reply_markup=get_main_menu(callback.from_user.language or "uz_latin")
        )
