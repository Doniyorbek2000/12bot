from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import AuditLog

class AuditRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def log_action(self, admin_id: int, action: str, entity_type: str, entity_id: Optional[int] = None, old_value_json: Optional[dict] = None, new_value_json: Optional[dict] = None) -> AuditLog:
        log = AuditLog(
            admin_id=admin_id,
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            old_value_json=old_value_json,
            new_value_json=new_value_json
        )
        self.db.add(log)
        await self.db.commit()
        return log

    async def get_latest_logs(self, limit: int = 50) -> List[AuditLog]:
        stmt = select(AuditLog).order_by(AuditLog.created_at.desc()).limit(limit)
        res = await self.db.execute(stmt)
        return list(res.scalars().all())
