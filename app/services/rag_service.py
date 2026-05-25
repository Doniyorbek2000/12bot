import logging
from typing import List, dict, Optional
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import LegalDocument, DocumentChunk, LegalSource
import google.generativeai as genai
from app.config import settings

logger = logging.getLogger("adolat_ai_bot.rag_service")

class RAGService:
    def __init__(self, db: AsyncSession):
        self.db = db
        # Configure Gemini embedding model
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.embedding_model = "models/text-embedding-004"

    async def generate_embedding(self, text_to_embed: str) -> Optional[List[float]]:
        """Gemini Embedding API orqali matnning vektor qiymatini (embedding) olish"""
        try:
            # Gemini embedding model request
            response = genai.embed_content(
                model=self.embedding_model,
                content=text_to_embed,
                task_type="retrieval_document"
            )
            return response.get("embedding")
        except Exception as e:
            logger.error(f"Embedding generatsiya qilishda xatolik: {e}")
            return None

    async def add_source(self, title: str, url: str, source_type: str = "lex_uz") -> LegalSource:
        """Yangi qonun manbasini qo'shish"""
        source = LegalSource(title=title, source_url=url, source_type=source_type)
        self.db.add(source)
        await self.db.flush()
        return source

    async def add_document_and_index(self, source_id: int, title: str, text_content: str, law_number: Optional[str] = None, article_number: Optional[str] = None) -> LegalDocument:
        """Yangi huquqiy hujjat qo'shish, bo'laklarga bo'lish va embedding vektorlarini yaratish"""
        doc = LegalDocument(
            source_id=source_id,
            title=title,
            text=text_content,
            law_number=law_number,
            article_number=article_number
        )
        self.db.add(doc)
        await self.db.flush()

        # Matnni bo'laklarga (chunks) bo'lish - oddiy paragraph split
        paragraphs = [p.strip() for p in text_content.split("\n\n") if p.strip()]
        
        for idx, para in enumerate(paragraphs):
            # Juda qisqa matnlarni tashlab ketamiz
            if len(para) < 20:
                continue
                
            # Embedding generatsiya qilish
            embedding = await self.generate_embedding(para)
            
            chunk = DocumentChunk(
                legal_document_id=doc.id,
                chunk_text=para,
                embedding=embedding,
                metadata_json={"paragraph_index": idx, "doc_title": title}
            )
            self.db.add(chunk)
        
        await self.db.commit()
        return doc

    async def search_relevant_chunks(self, query: str, limit: int = 3) -> List[dict]:
        """
        Foydalanuvchi so'roviga asosan eng mos keladigan qonun bo'laklarini semantik qidirish (pgvector).
        Agar pgvector faollashtirilgan bo'lsa, SQL kosinus o'xshashligini ishlatish mumkin.
        """
        try:
            query_vector = await self.generate_embedding(query)
            if not query_vector:
                return []

            # Agar pgvector kengaytmasi bazada o'rnatilgan bo'lsa va modelda Vector turi ishlatilsa
            # SQL: select * from document_chunks order by embedding <=> query_vector limit X
            # Hozircha SQL orqali asinxron yaqinlik qidiruvi misoli:
            vector_str = "[" + ",".join(map(str, query_vector)) + "]"
            
            # pgvector kosinus o'xshashlik so'rovi (SQL raw text yordamida pgvector ustidan qidirish)
            # Bu kelajakda Lex.uz ulanishi uchun tayyor yechimdir
            sql_query = text(
                "SELECT id, legal_document_id, chunk_text, (embedding <=> :vector) as distance "
                "FROM document_chunks "
                "ORDER BY embedding <=> :vector "
                "LIMIT :limit"
            )
            
            res = await self.db.execute(sql_query, {"vector": vector_str, "limit": limit})
            rows = res.fetchall()
            
            results = []
            for row in rows:
                results.append({
                    "id": row[0],
                    "doc_id": row[1],
                    "text": row[2],
                    "distance": row[3]
                })
            return results
            
        except Exception as e:
            logger.warning(f"pgvector semantik qidiruvida xatolik (Ehtimol pgvector extension hali faollashtirilmagan): {e}")
            
            # Fallback: Oddiy matnli (LIKE) qidiruv tizimi
            stmt = select(DocumentChunk).where(DocumentChunk.chunk_text.ilike(f"%{query}%")).limit(limit)
            res = await self.db.execute(stmt)
            chunks = res.scalars().all()
            return [{"id": c.id, "doc_id": c.legal_document_id, "text": c.chunk_text, "distance": 0.0} for c in chunks]
