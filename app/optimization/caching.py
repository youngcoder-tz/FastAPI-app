from redis import Redis
from functools import wraps
import pickle
from datetime import timedelta

class CacheManager:
    def __init__(self, redis: Redis):
        self.redis = redis

    def cache_response(self, key_prefix: str, ttl: int = 3600):
        def decorator(f):
            @wraps(f)
            async def wrapper(*args, **kwargs):
                cache_key = f"{key_prefix}:{str(kwargs)}"
                cached = self.redis.get(cache_key)
                if cached:
                    return pickle.loads(cached)
                
                result = await f(*args, **kwargs)
                self.redis.setex(cache_key, ttl, pickle.dumps(result))
                return result
            return wrapper
        return decorator

# Example usage in routes:
# @cache.cache_response("get_complaint")