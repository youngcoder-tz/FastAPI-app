from fastapi import Request
from fastapi.responses import JSONResponse

class AccessibilityMiddleware:
    async def __call__(self, request: Request, call_next):
        response = await call_next(request)
        
        # Check for accessibility headers
        if request.headers.get("X-Accessibility-Mode") == "high-contrast":
            inject_css(response, "high-contrast.css")
            
        if request.headers.get("X-Prefers-Text") == "simple":
            simplify_content(response)
            
        return response