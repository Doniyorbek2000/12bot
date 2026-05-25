from aiogram.fsm.state import StatesGroup, State

class UserStates(StatesGroup):
    # Til sozlamalari
    choosing_language = State()

    # Huquqiy savol-javob oqimi
    asking_legal_question = State()

    # Hujjat tahlili oqimi
    uploading_document = State()

    # Ovozli savol berish
    sending_voice = State()

    # Hujjat generatsiya qilish bosqichlari (Ariza/Shikoyat/Da'vo ariza)
    choosing_doc_type = State()
    
    # Quyidagi dynamic statelar orqali form-flow boshqariladi
    entering_doc_details = State()
