import os
import sys
import pytest

# Loyiha ildiz katalogini python pathga qo'shamiz
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_imports():
    """Barcha muhim modullar va kutubxonalar to'g'ri import bo'lishini tekshirish"""
    try:
        from app.config import settings
        from app.loader import bot, dp
        from app.db.database import Base, engine
        from app.db.models import User, Plan, Payment
        from app.services.gemini_service import GeminiService
        from app.services.legal_ai_service import LegalAIService
        from app.services.document_reader import DocumentReader
        from app.services.document_generator import DocumentGenerator
        from app.services.payment_service import PaymentService
        from app.services.click_service import ClickService
        from app.services.payme_service import PaymeService
        
        print("✅ Barcha modullar muvaffaqiyatli import qilindi!")
        assert True
    except Exception as e:
        print(f"❌ Import qilishda xatolik yuz berdi: {e}")
        assert False

def test_config_placeholders():
    """Placeholder konfiguratsiyalarni tekshirish"""
    from app.config import settings
    assert settings.DATABASE_URL is not None
    assert settings.REDIS_URL is not None

@pytest.mark.asyncio
async def test_document_reader_mock():
    """DocumentReader TXT decoder testi"""
    from app.services.document_reader import DocumentReader
    reader = DocumentReader()
    test_bytes = "O'zbekiston Respublikasi Konstitutsiyasi".encode("utf-8")
    res = reader.read_txt(test_bytes)
    assert res == "O'zbekiston Respublikasi Konstitutsiyasi"
