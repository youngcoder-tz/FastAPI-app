from sqlalchemy import Column, DateTime ,String, Text, Enum, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.database import Base
from enum import Enum as PyEnum

class PromiseStatus(str, PyEnum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    FULFILLED = "fulfilled"

class CampaignPromise(Base):
    __tablename__ = "campaign_promises"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    category = Column(String(255))
    status = Column(Enum(PromiseStatus), default=PromiseStatus.PENDING)
    politician_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    verified_by_journalist = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())