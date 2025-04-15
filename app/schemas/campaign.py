from pydantic import BaseModel
from datetime import datetime
from enum import Enum
from typing import Optional

class PromiseStatus(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    fulfilled = "fulfilled"

class CampaignPromiseBase(BaseModel):
    title: str
    description: str
    category: Optional[str] = None

class CampaignPromiseCreate(CampaignPromiseBase):
    pass

class CampaignPromiseUpdate(BaseModel):
    status: Optional[PromiseStatus] = None
    verified_by_journalist: Optional[bool] = None

class CampaignPromise(CampaignPromiseBase):
    id: str
    status: PromiseStatus
    politician_id: str
    created_at: datetime

    class Config:
        orm_mode = True