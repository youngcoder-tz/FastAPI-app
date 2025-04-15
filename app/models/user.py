import uuid
from sqlalchemy import Column, String, Boolean, Enum
from sqlalchemy.dialects.postgresql import UUID 
from app.database import Base
from enum import Enum as PyEnum

class UserRole(str, PyEnum):
    ADMIN = "admin"
    CITIZEN = "citizen"
    JOURNALIST = "journalist"
    DUTY_BEARER = "duty_bearer"
    CSO = "cso_access"

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.CITIZEN, nullable=False)
    is_verified = Column(Boolean, default=False)

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email})>"
