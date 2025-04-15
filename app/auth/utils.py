from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from app.config import settings

# Security
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# JWT Config
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE = 30  # minutes
REFRESH_TOKEN_EXPIRE = 7  # days

def create_tokens(data: dict):
    access_expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE)
    refresh_expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE)
    
    access_data = data.copy()
    access_data.update({"exp": access_expire})
    access_token = jwt.encode(access_data, SECRET_KEY, algorithm=ALGORITHM)

    refresh_data = data.copy()
    refresh_data.update({"exp": refresh_expire})
    refresh_token = jwt.encode(refresh_data, SECRET_KEY, algorithm=ALGORITHM)

    return {"access_token": access_token, "refresh_token": refresh_token}

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

def hash_password(password: str):
    return pwd_context.hash(password)