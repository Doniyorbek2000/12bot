from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from app.utils.texts import TEXTS

def get_language_keyboard() -> InlineKeyboardMarkup:
    """Tizimga kirganda tilni tanlash inline tugmalari"""
    keyboard = [
        [
            InlineKeyboardButton(text="🇺🇿 O'zbekcha", callback_data="set_lang_uz_latin"),
            InlineKeyboardButton(text="🇺🇿 Ўзбекча", callback_data="set_lang_uz_cyrillic")
        ],
        [
            InlineKeyboardButton(text="🇷🇺 Русский", callback_data="set_lang_ru")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_main_menu(lang: str = "uz_latin") -> ReplyKeyboardMarkup:
    """Asosiy menyu tugmalari (Reply Keyboard)"""
    btn = TEXTS["buttons"]
    
    keyboard = [
        [
            KeyboardButton(text=btn["ask_question"][lang]),
            KeyboardButton(text=btn["doc_analysis"][lang])
        ],
        [
            KeyboardButton(text=btn["doc_generation"][lang]),
            KeyboardButton(text=btn["voice_question"][lang])
        ],
        [
            KeyboardButton(text=btn["history"][lang]),
            KeyboardButton(text=btn["tariffs"][lang])
        ],
        [
            KeyboardButton(text=btn["profile"][lang]),
            KeyboardButton(text=btn["change_lang"][lang])
        ],
        [
            KeyboardButton(text=btn["help"][lang])
        ]
    ]
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        persistent=True,
        input_field_placeholder="Tanlang..."
    )

def get_back_keyboard(lang: str = "uz_latin") -> ReplyKeyboardMarkup:
    """Orqaga va Bosh menyu reply tugmasi"""
    btn = TEXTS["buttons"]
    keyboard = [
        [KeyboardButton(text=btn["back"][lang]), KeyboardButton(text=btn["main_menu"][lang])]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def get_cancel_inline(lang: str = "uz_latin") -> InlineKeyboardMarkup:
    """Bekor qilish inline tugmasi"""
    cancel_text = {
        "uz_latin": "❌ Bekor qilish",
        "uz_cyrillic": "❌ Бекор қилиш",
        "ru": "❌ Отменить"
    }
    keyboard = [
        [InlineKeyboardButton(text=cancel_text.get(lang, cancel_text["uz_latin"]), callback_data="cancel_action")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
