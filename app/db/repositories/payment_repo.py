from datetime import datetime
from typing import Optional, List
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.db.models import Payment

class PaymentRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_payment(self, user_id: int, plan_id: int, amount: float, provider: str = "mock", invoice_id: Optional[str] = None) -> Payment:
        payment = Payment(
            user_id=user_id,
            plan_id=plan_id,
            amount=amount,
            provider=provider,
            invoice_id=invoice_id,
            status="pending"
        )
        self.db.add(payment)
        await self.db.commit()
        return payment

    async def get_by_invoice_id(self, invoice_id: str) -> Optional[Payment]:
        stmt = (
            select(Payment)
            .where(Payment.invoice_id == invoice_id)
            .options(
                selectinload(Payment.user),
                selectinload(Payment.plan)
            )
        )
        res = await self.db.execute(stmt)
        return res.scalars().first()

    async def get_by_provider_transaction_id(self, provider: str, tx_id: str) -> Optional[Payment]:
        stmt = (
            select(Payment)
            .where((Payment.provider == provider) & (Payment.provider_transaction_id == tx_id))
            .options(
                selectinload(Payment.user),
                selectinload(Payment.plan)
            )
        )
        res = await self.db.execute(stmt)
        return res.scalars().first()

    async def mark_as_paid(self, payment_id: int, provider_transaction_id: str, raw_payload: Optional[dict] = None) -> Optional[Payment]:
        stmt = (
            select(Payment)
            .where(Payment.id == payment_id)
            .options(
                selectinload(Payment.user),
                selectinload(Payment.plan)
            )
        )
        res = await self.db.execute(stmt)
        payment = res.scalars().first()

        if payment and payment.status != "paid":
            payment.status = "paid"
            payment.provider_transaction_id = provider_transaction_id
            payment.raw_payload_json = raw_payload
            payment.paid_at = datetime.utcnow()
            await self.db.commit()
        return payment

    async def mark_as_failed(self, payment_id: int, raw_payload: Optional[dict] = None) -> None:
        stmt = update(Payment).where(Payment.id == payment_id).values(status="failed", raw_payload_json=raw_payload)
        await self.db.execute(stmt)
        await self.db.commit()

    async def get_all_payments(self, status: Optional[str] = None) -> List[Payment]:
        stmt = select(Payment).options(selectinload(Payment.user), selectinload(Payment.plan)).order_by(Payment.created_at.desc())
        if status:
            stmt = stmt.where(Payment.status == status)
        res = await self.db.execute(stmt)
        return list(res.scalars().all())
