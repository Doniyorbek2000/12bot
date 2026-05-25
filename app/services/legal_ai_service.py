from typing import Optional
from app.services.gemini_service import GeminiService

class LegalAIService:
    def __init__(self, gemini_service: GeminiService):
        self.gemini = gemini_service

    async def answer_legal_question(self, question: str, lang: str = "uz_latin") -> dict:
        """Huquqiy savolga O'zbekiston qonunchiligi asosida javob olish"""
        
        # Til bo'yicha ehtiyotkorlik xulosasi
        disclaimers = {
            "uz_latin": "\n\n⚠️ <i>Ehtiyotkorlik ogohlantirishi: Ushbu javob faqat ma'lumot berish xarakteriga ega va rasmiy advokatlik yoki yuridik maslahat o'rnini bosmaydi. Zaruriyat bo'lganda, malakali yuristga yoki advokatga murojaat qilish tavsiya etiladi.</i>",
            "uz_cyrillic": "\n\n⚠️ <i>Эҳтиёткорлик огоҳлантириши: Ушбу жавоб фақат маълумот бериш характерига эга ва расмий адвокатлик ёки юридик маслаҳат ўрнини босмайди. Зарурият бўлганда, малакали юристга ёки адвокатга мурожаат қилиш тавсия этилади.</i>",
            "ru": "\n\n⚠️ <i>Предупреждение: Данный ответ носит исключительно информационный характер и не заменяет официальную юридическую консультацию или помощь адвоката. При необходимости рекомендуется обратиться к квалифицированному юристу.</i>"
        }
        
        # Prompt yaratish
        prompt = (
            f"Foydalanuvchi savoli: {question}\n\n"
            f"Savolga O'zbekiston Respublikasi qonunchiligi (va zarur bo'lsa xalqaro huquq normalari) doirasida mukammal, sodda va tushunarli tilda javob ber. "
            f"Javob tuzilishi quyidagicha bo'lishi shart:\n"
            f"1. 📌 Qisqa xulosa\n"
            f"2. ⚖️ Huquqiy asos (Qaysi qonun, kodeks yoki moddaga asosan? Manbasini aniq ko'rsat. Agar aniq bo'lmasa, 'aniq manba topilmadi' deb yoz)\n"
            f"3. 💡 Siz nima qilishingiz mumkin? (Foydalanuvchi uchun amaliy yechimlar)\n"
            f"4. 📂 Kerakli hujjatlar (Agar ushbu holat uchun hujjat topshirish kerak bo'lsa)\n"
            f"5. ⚠️ Ehtiyotkorlik choralari (Sud, aliment, mehnat nizolari kabi katta xavfli masalalarda alohida ogohlantirish)\n"
            f"6. ➔ Keyingi qadam (Foydalanuvchi birinchi navbatda qaerga borishi yoki nima qilishi kerak?)\n\n"
            f"Javobni foydalanuvchi tilida yoz. Til kodi: {lang}."
        )

        res = await self.gemini.generate_response(prompt, temperature=0.3)
        if res["status"] == "success":
            res["text"] += disclaimers.get(lang, disclaimers["uz_latin"])
        return res

    async def analyze_document(self, doc_text: str, file_name: str, lang: str = "uz_latin") -> dict:
        """Hujjat matnini tahlil qilish uchun Gemini API ga yuborish"""
        
        system_instruction = (
            "Sen yuqori malakali, O'zbekiston qonunchiligini mukammal biladigan huquqshunos AIsan. "
            "Sening vazifang foydalanuvchi yuborgan hujjat matnini tahlil qilish va undagi huquqiy xavf-xatarlarni, "
            "majburiyatlarni va huquqlarni aniqlashdir. Javobing tushunarli, sodda va professional huquqiy uslubda bo'lsin."
        )
        
        prompt = (
            f"Hujjat nomi: {file_name}\n"
            f"Hujjat matni:\n{doc_text}\n\n"
            f"Ushbu hujjatni O'zbekiston Respublikasi qonunchiligi asosida tahlil qil va quyidagi tuzilmada javob ber:\n"
            f"1. 📄 Hujjatning umumiy mazmuni va turi\n"
            f"2. 📌 Muhim va asosiy bandlar\n"
            f"3. ⚠️ Foydalanuvchi uchun xavfli yoki noqulay bo'lgan joylar (masalan: muddati o'tgan jarimalar, asossiz majburiyatlar)\n"
            f"4. 🔍 Alohida e'tibor qaratish lozim bo'lgan bandlar\n"
            f"5. ⚖️ Foydalanuvchining huquqlari va majburiyatlari (taraflar majburiyatlari muvozanati)\n"
            f"6. 💡 Tavsiya qilinadigan keyingi amaliy qadamlar\n"
            f"7. 🤝 Professional yurist/advokat bilan bevosita maslahatlashish kerak bo'lgan vaziyatlar\n\n"
            f"Javobni foydalanuvchi tilida qaytar. Til kodi: {lang}."
        )

        return await self.gemini.generate_response(prompt, system_instruction=system_instruction, temperature=0.2)

    async def generate_document(self, doc_type: str, info: dict, lang: str = "uz_latin") -> dict:
        """Hujjat ma'lumotlari asosida tayyor huquqiy hujjat matnini tayyorlash"""
        
        system_instruction = (
            "Sen rasmiy hujjatlar (ariza, shikoyat, da'vo arizasi va boshqalar) yozish bo'yicha mutaxassis AIsan. "
            "Sen foydalanuvchi bergan ma'lumotlar asosida mukammal, imloviy va huquqiy xatolarsiz rasmiy hujjat tayyorlaysan. "
            "Hujjat O'zbekiston amaliyotida qo'llaniladigan rasmiy andozalarga to'liq mos bo'lishi kerak. Murakkab va tushunarsiz iboralarni kamaytir."
        )
        
        # Info dictionaryni formatlash
        details_str = ""
        for key, val in info.items():
            details_str += f"- {key}: {val}\n"

        prompt = (
            f"Tayyorlanishi kerak bo'lgan hujjat turi: {doc_type}\n"
            f"Foydalanuvchi kiritgan ma'lumotlar:\n{details_str}\n"
            f"Ushbu ma'lumotlar asosida rasmiy huquqiy hujjat matnini to'liq shaklda tayyorla.\n"
            f"Hujjat tuzilishi quyidagicha bo'lishi shart:\n"
            f"- Yuqori o'ng burchakda: Kimga (qabul qiluvchi) va Kimdan (yuboruvchi - F.I.Sh., manzil, telefon)\n"
            f"- O'rtada: Hujjat nomi (masalan: ARIZA, SHIKOYAT, DA'VO ARIZASI)\n"
            f"- Asosiy qism: Holatning huquqiy va faktik tavsifi, O'zbekiston qonunlariga (moddalariga) asoslangan asoslar\n"
            f"- Talab yoki iltimos: Foydalanuvchining aniq talabi\n"
            f"- Ilovalar ro'yxati (agar bor bo'lsa)\n"
            f"- Pastda: Sana va imzo joyi\n\n"
            f"Diqqat: Hujjat ichida to'ldirilishi kerak bo'lgan joylar bo'lsa [ ] qavs ichida ko'rsat. "
            f"Hujjat faqat professional va rasmiy huquqiy tilda bo'lsin. Javobni foydalanuvchi tilida ber. Til kodi: {lang}."
        )

        return await self.gemini.generate_response(prompt, system_instruction=system_instruction, temperature=0.1)
