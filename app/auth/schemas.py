from pydantic import BaseModel, EmailStr, Field, validator
from enum import Enum
from typing import Optional
from datetime import datetime

# ---------- Enums ----------
class UserRole(str, Enum):
    ADMIN = "admin"
    CITIZEN = "citizen"
    JOURNALIST = "journalist"
    DUTY_BEARER = "duty_bearer"
    CSO = "cso_access"

# ---------- Token Schemas ----------
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    email: Optional[str] = None
    role: Optional[UserRole] = None

# ---------- Auth Request Schemas ----------
class UserSignUp(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, example="SecurePassword123!")
    role: UserRole = UserRole.CITIZEN
    token_code: Optional[str] = None  # For CSO/Duty Bearer role assignment

    @validator("password")
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one digit")
        return v

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class PasswordResetRequest(BaseModel):
    email: EmailStr

class PasswordResetConfirm(BaseModel):
    new_password: str = Field(..., min_length=8)
    reset_token: str

# ---------- Response Schemas ----------
class UserBase(BaseModel):
    email: EmailStr
    role: UserRole
    is_verified: bool

class UserResponse(UserBase):
    id: str
    created_at: datetime

    class Config:
        orm_mode = True

class JournalistVerificationRequest(BaseModel):
    social_media_id_url: str = Field(
        ...,
        example="https://example.com/id.jpg",
        description="URL to journalist's social media ID card"
    )

# ---------- Admin Schemas ----------
class AdminUserUpdate(BaseModel):
    role: Optional[UserRole]
    is_verified: Optional[bool]