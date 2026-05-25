from aiogram.fsm.state import StatesGroup, State

class AdminStates(StatesGroup):
    # Foydalanuvchilarni boshqarish
    searching_user = State()
    giving_plan = State()
    adding_limit = State()
    blocking_user = State()

    # Promo-kodlar yaratish
    creating_promo_code = State()
    entering_promo_discount = State()
    entering_promo_plan = State()

    # Broadcast xabar yuborish
    writing_broadcast_message = State()
    confirming_broadcast = State()

    # AI sozlamalarini o'zgartirish
    modifying_system_prompt = State()
    modifying_model_name = State()
