from fastapi import Request
import time
from prometheus_client import Histogram

REQUEST_TIME = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration',
    ['method', 'path']
)

async def track_performance(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    
    REQUEST_TIME.labels(
        method=request.method,
        path=request.url.path
    ).observe(duration)
    
    response.headers["X-Process-Time"] = str(duration)
    return response