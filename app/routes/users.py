from fastapi import APIRouter, Depends
from app.auth.dependencies import get_current_user
from app.models.user import User
from app.database import SessionLocal

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/me")
def get_my_profile(current_user: dict = Depends(get_current_user)):
    db = SessionLocal()
    user = db.query(User).filter(User.email == current_user["sub"]).first()
    return user