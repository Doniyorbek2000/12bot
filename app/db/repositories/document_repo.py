from typing import List, Optional
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.db.models import UploadedDocument, GeneratedDocument

class DocumentRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    # Yuklangan Hujjatlar
    async def create_uploaded_document(self, user_id: int, telegram_file_id: str, file_name: str, file_type: str, file_size: int) -> UploadedDocument:
        doc = UploadedDocument(
            user_id=user_id,
            telegram_file_id=telegram_file_id,
            file_name=file_name,
            file_type=file_type,
            file_size=file_size,
            status="uploaded"
        )
        self.db.add(doc)
        await self.db.commit()
        return doc

    async def update_analysis_result(self, doc_id: int, extracted_text: str, analysis_result: str, status: str = "analyzed") -> Optional[UploadedDocument]:
        stmt = (
            update(UploadedDocument)
            .where(UploadedDocument.id == doc_id)
            .values(
                extracted_text=extracted_text,
                analysis_result=analysis_result,
                status=status
            )
        )
        await self.db.execute(stmt)
        await self.db.commit()
        
        stmt_select = select(UploadedDocument).where(UploadedDocument.id == doc_id)
        res = await self.db.execute(stmt_select)
        return res.scalars().first()

    async def get_uploaded_by_user(self, user_id: int, limit: int = 5) -> List[UploadedDocument]:
        stmt = select(UploadedDocument).where(UploadedDocument.user_id == user_id).order_by(UploadedDocument.created_at.desc()).limit(limit)
        res = await self.db.execute(stmt)
        return list(res.scalars().all())

    # Generatsiya qilingan Hujjatlar
    async def create_generated_document(self, user_id: int, document_type: str, input_data_json: dict, generated_text: str, docx_path: Optional[str] = None, pdf_path: Optional[str] = None, status: str = "generated") -> GeneratedDocument:
        doc = GeneratedDocument(
            user_id=user_id,
            document_type=document_type,
            input_data_json=input_data_json,
            generated_text=generated_text,
            docx_path=docx_path,
            pdf_path=pdf_path,
            status=status
        )
        self.db.add(doc)
        await self.db.commit()
        return doc

    async def get_generated_by_user(self, user_id: int, limit: int = 5) -> List[GeneratedDocument]:
        stmt = select(GeneratedDocument).where(GeneratedDocument.user_id == user_id).order_by(GeneratedDocument.created_at.desc()).limit(limit)
        res = await self.db.execute(stmt)
        return list(res.scalars().all())

    async def get_all_uploaded(self) -> List[UploadedDocument]:
        stmt = select(UploadedDocument).options(selectinload(UploadedDocument.user)).order_by(UploadedDocument.created_at.desc())
        res = await self.db.execute(stmt)
        return list(res.scalars().all())
