from redis import Redis

def get_redis():
    return Redis(host='redis', port=6379, db=0)

def get_ai_service(redis: Redis = Depends(get_redis)):
    return CachedAIService(redis)