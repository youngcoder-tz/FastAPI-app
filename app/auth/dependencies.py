from fastapi import Depends, HTTPException, status
from jose import jwt , JWTError
from app.auth.utils import oauth2_scheme, SECRET_KEY, ALGORITHM
from app.models.user import UserRole

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

def require_role(role: UserRole):
    def role_checker(current_user: dict = Depends(get_current_user)):
        if current_user.get("role") != role.value:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Role {role.value} required",
            )
        return current_user
    return role_checker