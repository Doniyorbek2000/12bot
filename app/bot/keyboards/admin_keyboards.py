from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

def get_admin_menu() -> ReplyKeyboardMarkup:
    """Admin Asosiy Menyusi (Reply Keyboard)"""
    keyboard = [
        [
            KeyboardButton(text="📊 Dashboard"),
            KeyboardButton(text="👥 Foydalanuvchilar")
        ],
        [
            KeyboardButton(text="💬 Savollar tarixi"),
            KeyboardButton(text="📄 Hujjat tahlillari")
        ],
        [
            KeyboardButton(text="📝 Tayyorlangan hujjatlar"),
            KeyboardButton(text="💳 To'lovlar")
        ],
        [
            KeyboardButton(text="🧾 Tariflar"),
            KeyboardButton(text="🎁 Promo kodlar")
        ],
        [
            KeyboardButton(text="📢 Xabar yuborish"),
            KeyboardButton(text="⚙️ AI sozlamalari")
        ],
        [
            KeyboardButton(text="🚫 Bloklanganlar"),
            KeyboardButton(text="📜 Audit log")
        ],
        [
            KeyboardButton(text="🏠 Foydalanuvchi menyusi")
        ]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def get_payment_approval_keyboard(invoice_id: str) -> InlineKeyboardMarkup:
    """Admin to'lovni qo'lda tasdiqlashi uchun inline tugmalar"""
    keyboard = [
        [
            InlineKeyboardButton(text="✅ Tasdiqlash", callback_data=f"admin_approve_pay_{invoice_id}"),
            InlineKeyboardButton(text="❌ Rad etish", callback_data=f"admin_reject_pay_{invoice_id}")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_user_manage_keyboard(telegram_id: int, is_blocked: bool = False) -> InlineKeyboardMarkup:
    """Admin foydalanuvchini boshqarishi uchun inline tugmalar"""
    block_btn = InlineKeyboardButton(text="✅ Blokdan chiqarish", callback_data=f"admin_unblock_user_{telegram_id}") if is_blocked else InlineKeyboardButton(text="🚫 Bloklash", callback_data=f"admin_block_user_{telegram_id}")
    
    keyboard = [
        [
            InlineKeyboardButton(text="🧾 Tarif berish", callback_data=f"admin_give_plan_{telegram_id}"),
            InlineKeyboardButton(text="➕ Limit qo'shish", callback_data=f"admin_add_limit_{telegram_id}")
        ],
        [
            block_btn
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_admin_plans_keyboard() -> InlineKeyboardMarkup:
    """Admin plan tanlashi uchun inline tugmalar (foydalanuvchiga plan biriktirishda)"""
    keyboard = [
        [
            InlineKeyboardButton(text="FREE", callback_data="admin_assign_plan_FREE"),
            InlineKeyboardButton(text="ODDIY", callback_data="admin_assign_plan_ODDIY")
        ],
        [
            InlineKeyboardButton(text="PRO", callback_data="admin_assign_plan_PRO"),
            InlineKeyboardButton(text="STANDART", callback_data="admin_assign_plan_STANDART")
        ],
        [
            InlineKeyboardButton(text="ULTRA", callback_data="admin_assign_plan_ULTRA"),
            InlineKeyboardButton(text="VIP", callback_data="admin_assign_plan_VIP")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
