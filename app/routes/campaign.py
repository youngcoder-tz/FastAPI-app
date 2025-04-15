from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.campaign import CampaignPromise
from app.schemas.campaign import CampaignPromiseCreate, CampaignPromise
from app.auth.dependencies import get_current_user, require_role
from app.models.user import UserRole

router = APIRouter(prefix="/campaign-promises", tags=["campaign_promises"])

@router.post("/", response_model=CampaignPromise)
def create_promise(
    promise: CampaignPromiseCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role(UserRole.JOURNALIST))
):
    db_promise = CampaignPromise(
        **promise.dict(),
        politician_id=current_user["sub"],
        status="pending"
    )
    db.add(db_promise)
    db.commit()
    db.refresh(db_promise)
    return db_promise