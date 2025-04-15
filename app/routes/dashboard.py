from fastapi import APIRouter
from fastapi_cache.decorator import cache

router = APIRouter(prefix="/dashboard", tags=["Public Dashboard"])

@router.get("/sentiment")
@cache(expire=3600)  # 1 hour cache
async def public_sentiment(
    timeframe: str = "7d",
    location: str = None
):
    """
    Returns:
    {
        "positive": 0.65,
        "negative": 0.22,
        "neutral": 0.13,
        "trend": "improving"  
    }
    """
    df = get_sentiment_data(timeframe, location)
    return {
        "positive": (df['polarity'] > 0.3).mean(),
        "negative": (df['polarity'] < -0.3).mean(),
        "neutral": ((df['polarity'] >= -0.3) & (df['polarity'] <= 0.3)).mean(),
        "trend": calculate_trend(df)
    }

@router.get("/promise-tracker")
async def promise_tracker(politician_id: UUID = None):
    """Visualization-ready promise fulfillment data"""
    return {
        "fulfilled": count_fulfilled_promises(politician_id),
        "in_progress": count_in_progress_promises(politician_id),
        "broken": count_broken_promises(politician_id),
        "average_days": avg_completion_time(politician_id)
    }