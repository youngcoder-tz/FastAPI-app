from fastapi import APIRouter, Depends ,HTTPException
from app.auth.dependencies import require_role, get_current_user
from app.models.user import User, UserRole
from app.database import SessionLocal

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.patch("/verify-journalist/{user_id}")
def verify_journalist(
    user_id: str,
    current_user: dict = Depends(require_role(UserRole.ADMIN))
):
    db = SessionLocal()
    user = db.query(User).filter(User.id == user_id, User.role == UserRole.JOURNALIST).first()
    if not user:
        raise HTTPException(status_code=404, detail="Journalist not found")
    
    user.is_verified = True
    db.commit()
    return {"message": "Journalist verified"}