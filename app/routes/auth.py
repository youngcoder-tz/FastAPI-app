from fastapi import APIRouter, Depends, HTTPException
from app.auth.utils import create_tokens, hash_password, verify_password
from app.auth.schemas import UserSignUp, UserLogin, Token, UserResponse
from app.auth.dependencies import get_current_user
from app.models.user import User
from app.database import SessionLocal

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/signup", response_model=Token)
async def signup(user_data: UserSignUp):
    db = SessionLocal()
    # Check if user exists
    if db.query(User).filter(User.email == user_data.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Hash password and create user
    hashed_password = hash_password(user_data.password)
    user = User(email=user_data.email, hashed_password=hashed_password, role=user_data.role)
    db.add(user)
    db.commit()
    
    # Generate tokens
    tokens = create_tokens({"sub": user.email, "role": user.role})
    return tokens


@router.post("/login", response_model=Token)
async def login(credentials: UserLogin):
    db = SessionLocal()
    user = db.query(User).filter(User.email == credentials.email).first()
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    return create_tokens({"sub": user.email, "role": user.role})


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user