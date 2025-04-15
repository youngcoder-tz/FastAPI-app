from pydantic import BaseModel
from datetime import datetime
from enum import Enum
from typing import Optional

class ComplaintStatus(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    resolved = "resolved"

class ComplaintBase(BaseModel):
    title: str
    description: str
    location: Optional[str] = None

class ComplaintCreate(ComplaintBase):
    pass

class ComplaintUpdate(BaseModel):
    status: Optional[ComplaintStatus] = None
    assigned_to: Optional[str] = None

class Complaint(ComplaintBase):
    id: str
    status: ComplaintStatus
    citizen_id: str
    created_at: datetime

    class Config:
        orm_mode = True