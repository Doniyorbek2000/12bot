# Static texts for Multi-language support (uz_latin, uz_cyrillic, ru)

TEXTS = {
    "welcome": {
        "uz_latin": (
            "⚖️ <b>“Adolat AI” huquqiy yordamchi botiga xush kelibsiz!</b>\n\n"
            "Ushbu bot O'zbekiston Respublikasi qonunchiligi asosida sizga huquqiy maslahat berish, "
            "hujjatlarni tahlil qilish va turli xil arizalar, shikoyatlar tayyorlashda yordam beradi.\n\n"
            "<i>Iltimos, davom etish uchun quyidagi menyudan o'zingizga qulay tilni tanlang:</i>"
        ),
        "uz_cyrillic": (
            "⚖️ <b>“Адолат АI” ҳуқуқий ёрдамчи ботига хуш келибсиз!</b>\n\n"
            "Ушбу бот Ўзбекистон Республикаси қонунчилиги асосида сизга ҳуқуқий маслаҳат бериш, "
            "ҳужжатларни таҳлил қилиш ва турли хил аризалар, шикоятлар тайёрлашда ёрдам беради.\n\n"
            "<i>Илтимос, давом этиш учун қуйидаги менюдан ўзингизга қулай тилни танланг:</i>"
        ),
        "ru": (
            "⚖️ <b>Добро пожаловать в юридический бот-помощник «Adolat AI»!</b>\n\n"
            "Этот бот поможет вам получить юридическую консультацию, проанализировать документы "
            "и подготовить заявления или жалобы на основе законодательства Республики Узбекистан.\n\n"
            "<i>Пожалуйста, выберите удобный для вас язык из меню ниже для продолжения:</i>"
        )
    },
    "main_menu_text": {
        "uz_latin": "🏠 <b>Bosh menyu.</b> Kerakli bo'limni tanlang:",
        "uz_cyrillic": "🏠 <b>Бош меню.</b> Керакли бўлимни танланг:",
        "ru": "🏠 <b>Главное меню.</b> Выберите нужный раздел:"
    },
    "buttons": {
        "ask_question": {
            "uz_latin": "⚖️ Huquqiy savol berish",
            "uz_cyrillic": "⚖️ Ҳуқуқий савол бериш",
            "ru": "⚖️ Задать юр. вопрос"
        },
        "doc_analysis": {
            "uz_latin": "📄 Hujjat tahlil qilish",
            "uz_cyrillic": "📄 Ҳужжат таҳлил қилиш",
            "ru": "📄 Анализ документа"
        },
        "doc_generation": {
            "uz_latin": "📝 Hujjat tayyorlash",
            "uz_cyrillic": "📝 Ҳужжат тайёрлаш",
            "ru": "📝 Подготовить документ"
        },
        "voice_question": {
            "uz_latin": "🎙 Ovozli savol",
            "uz_cyrillic": "🎙 Овозли савол",
            "ru": "🎙 Голосовой вопрос"
        },
        "history": {
            "uz_latin": "📚 Mening tarixim",
            "uz_cyrillic": "📚 Менинг тарихим",
            "ru": "📚 Моя история"
        },
        "tariffs": {
            "uz_latin": "💳 Tariflar va to'lov",
            "uz_cyrillic": "💳 Тарифлар ва тўлов",
            "ru": "💳 Тарифы и оплата"
        },
        "profile": {
            "uz_latin": "👤 Profilim",
            "uz_cyrillic": "👤 Профилим",
            "ru": "👤 Мой профиль"
        },
        "change_lang": {
            "uz_latin": "🌐 Tilni o'zgartirish",
            "uz_cyrillic": "🌐 Тилни ўзгартириш",
            "ru": "🌐 Изменить язык"
        },
        "help": {
            "uz_latin": "🆘 Yordam",
            "uz_cyrillic": "🆘 Ёрдам",
            "ru": "🆘 Помощь"
        },
        "back": {
            "uz_latin": "⬅️ Orqaga",
            "uz_cyrillic": "⬅️ Орқага",
            "ru": "⬅️ Назад"
        },
        "main_menu": {
            "uz_latin": "🏠 Bosh menyu",
            "uz_cyrillic": "🏠 Бош меню",
            "ru": "🏠 Главное меню"
        }
    },
    "ask_question_prompt": {
        "uz_latin": (
            "⚖️ <b>Huquqiy savol yozish bo'limi</b>\n\n"
            "O'zingizni qiziqtirgan huquqiy muammoni yoki savolni batafsil matn ko'rinishida yozib yuboring.\n"
            "Sun'iy intellekt savolingizni tahlil qilib, qonun normalari asosida javob beradi.\n\n"
            "<i>(Masalan: \"Men ish beruvchidan oylik maoshimni 2 oydan beri ololmayapman, nima qilishim kerak?\")</i>"
        ),
        "uz_cyrillic": (
            "⚖️ <b>Ҳуқуқий савол ёзиш бўлими</b>\n\n"
            "Ўзингизни қизиқтирган ҳуқуқий муаммони ёки саволни батафсил матн кўринишида ёзиб юборинг.\n"
            "Сунъий интеллект саволингизни таҳлил қилиб, қонун нормалари асосида жавоб беради.\n\n"
            "<i>(Масалан: \"Мен иш берувчидан ойлик маошимни 2 ойдан бери ололмаяпман, нима қилишим керак?\")</i>"
        ),
        "ru": (
            "⚖️ <b>Раздел юридических вопросов</b>\n\n"
            "Пожалуйста, подробно опишите вашу юридическую проблему или вопрос в текстовом виде.\n"
            "Искусственный интеллект проанализирует ваш вопрос и ответит на основе законов.\n\n"
            "<i>(Например: «Работодатель не выплачивает мне зарплату уже 2 месяца, что делать?»)</i>"
        )
    },
    "doc_analysis_prompt": {
        "uz_latin": (
            "📄 <b>Hujjatlarni tahlil qilish bo'limi</b>\n\n"
            "Iltimos, tahlil qilinishi kerak bo'lgan hujjatni (shartnoma, bitim, ariza va b.) <b>PDF, DOCX yoki TXT</b> formatida yuboring.\n"
            "Tizim hujjatni o'qib, undagi huquqiy xavfli bandlar va tavsiyalarni aniqlab beradi.\n\n"
            "⚠️ <i>Maksimal fayl hajmi joriy tarifingizga bog'liq.</i>"
        ),
        "uz_cyrillic": (
            "📄 <b>Ҳужжатларни таҳлил қилиш бўлими</b>\n\n"
            "Илтимос, таҳлил қилиниши керак бўлган ҳужжатни (шартнома, битим, ариза ва б.) <b>PDF, DOCX ёки TXT</b> форматида юборинг.\n"
            "Тизим ҳужжатни ўқиб, ундаги ҳуқуқий хавфли бандлар ва тавсияларни аниқлаб беради.\n\n"
            "⚠️ <i>Максимал файл ҳажми жорий тарифингизга боғлиқ.</i>"
        ),
        "ru": (
            "📄 <b>Раздел анализа документов</b>\n\n"
            "Пожалуйста, отправьте документ (договор, соглашение, заявление и др.) в формате <b>PDF, DOCX или TXT</b>.\n"
            "Система изучит документ, выявит юридические риски для вас и предоставит рекомендации.\n\n"
            "⚠️ <i>Максимальный размер файла зависит от вашего тарифа.</i>"
        )
    },
    "voice_prompt": {
        "uz_latin": (
            "🎙 <b>Ovozli savol berish bo'limi</b>\n\n"
            "O'zingizni qiziqtirgan huquqiy savolni ovozli xabar (voice message) orqali yozib yuboring.\n"
            "Tizim ovozingizni matnga aylantirib, so'ng huquqiy javob beradi.\n\n"
            "⚠️ <i>Ushbu xizmat faqat <b>PRO</b> va undan yuqori tariflarda ishlaydi.</i>"
        ),
        "uz_cyrillic": (
            "🎙 <b>Овозли савол бериш бўлими</b>\n\n"
            "Ўзингизни қизиқтирган ҳуқуқий саволни овозли хабар (voice message) орқали ёзиб юборинг.\n"
            "Тизим овозингизни матнга айлантириб, сўнг ҳуқуқий жавоб беради.\n\n"
            "⚠️ <i>Ушбу хизмат фақат <b>PRO</b> ва ундан юқори тарифларда ишлайди.</i>"
        ),
        "ru": (
            "🎙 <b>Раздел голосовых вопросов</b>\n\n"
            "Отправьте свой юридический вопрос в виде голосового сообщения (voice message).\n"
            "Система преобразует ваш голос в текст, а затем предоставит юридический ответ.\n\n"
            "⚠️ <i>Эта функция доступна только для тарифов <b>PRO</b> и выше.</i>"
        )
    },
    "help_text": {
        "uz_latin": (
            "🆘 <b>Tizimdan foydalanish yo'riqnomasi</b>\n\n"
            "1️⃣ <b>Huquqiy savol berish</b>: Istalgan vaqtda matn ko'rinishida savol bering. Tizim qonunchilik asosida javob beradi.\n"
            "2️⃣ <b>Hujjat tahlili</b>: Shartnomalarni yuklang, undagi yashirin xavflarni va foydangizga ishlaydigan bandlarni bilib oling.\n"
            "3️⃣ <b>Hujjat yaratish</b>: Bir necha bosqichli savollarga javob berib, rasmiy ariza, shikoyat yoki da'vo arizasini tayyorlang.\n"
            "4️⃣ <b>Tariflar</b>: Limitlaringiz tugasa, menyudan tegishli tarifni tanlab, Click/Payme orqali to'lovni bajaring.\n\n"
            "⚠️ <b>Huquqiy ogohlantirish</b>: Tizim sun'iy intellekt yordamida ishlaydi va uning javoblari 100% mutloq hisoblanmaydi. Muhim va katta nizolarda professional advokatlarga murojaat qilishingiz shart.\n\n"
            "📞 <b>Aloqa</b>: Muammolar yuzasidan adminimizga murojaat qiling: @AdolatAI_Support"
        ),
        "uz_cyrillic": (
            "🆘 <b>Тизимдан фойдаланиш йўриқномаси</b>\n\n"
            "1️⃣ <b>Ҳуқуқий савол бериш</b>: Исталган вақтда матн кўринишида савол беринг. Тизим қонунчилик асосида жавоб беради.\n"
            "2️⃣ <b>Ҳужжат таҳлили</b>: Шартномаларни юкланг, ундаги яширин хавфларни ва фойдангизга ишлайдиган бандларни билиб олинг.\n"
            "3️⃣ <b>Ҳужжат яратиш</b>: Бир неча босқичли саволларга жавоб бериб, расмий ариза, шикоят ёки даъво аризасини тайёрланг.\n"
            "4️⃣ <b>Тарифлар</b>: Лимитларингиз тугаса, менюдан тегишли тарифни танаб, Click/Payme орқали тўловни бажаринг.\n\n"
            "⚠️ <b>Ҳуқуқий огоҳлантириш</b>: Тизим сунъий интеллект ёрдамида ишлайди ва унинг жавоблари 100% мутлоқ ҳисобланмайди. Муҳим ва катта низоларда профессионал адвокатларга мурожаат қилишингиз шарт.\n\n"
            "📞 <b>Алоқа</b>: Муаммолар юзасидан админимизга мурожаат қилинг: @AdolatAI_Support"
        ),
        "ru": (
            "🆘 <b>Инструкция по использованию системы</b>\n\n"
            "1️⃣ <b>Задать вопрос</b>: Напишите свой вопрос. Бот найдет правовую основу в законах и даст ответ.\n"
            "2️⃣ <b>Анализ документов</b>: Отправьте договор, чтобы узнать скрытые риски и обязательства.\n"
            "3️⃣ <b>Создание документов</b>: Ответьте на несколько вопросов бота, чтобы сгенерировать готовое заявление, жалобу или иск.\n"
            "4️⃣ <b>Тарифы</b>: При исчерпании лимитов выберите тариф и оплатите его через Click/Payme.\n\n"
            "⚠️ <b>Правовое предупреждение</b>: Бот работает на базе ИИ. Ответы не являются окончательным вердиктом адвоката. В случае серьезных споров обратитесь к юристу.\n\n"
            "📞  <b>Поддержка</b>: По всем вопросам пишите администратору: @AdolatAI_Support"
        )
    }
}
