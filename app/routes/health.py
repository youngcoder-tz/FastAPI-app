from fastapi import APIRouter
from redis import Redis
from sqlalchemy import text
from app.database import SessionLocal

router = APIRouter()

@router.get("/health")
async def health_check():
    return {"status": "ok"}

@router.get("/health/db")
async def db_health():
    db = SessionLocal()
    try:
        db.execute(text("SELECT 1"))
        return {"database": "ok"}
    except Exception as e:
        return {"database": str(e)}
    finally:
        db.close()

@router.get("/health/redis")
async def redis_health(redis: Redis = Depends(get_redis)):
    try:
        redis.ping()
        return {"redis": "ok"}
    except Exception as e:
        return {"redis": str(e)}