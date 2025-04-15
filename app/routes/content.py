from fastapi import APIRouter, Depends, Request, Query ,HTTPException
from app.services.translation import UITranslator

router = APIRouter(prefix="/content", tags=["content"])

BASE_CONTENT = {
    "welcome_message": "Welcome to Wajibika",
    "complaint_instructions": "Describe your issue...",
    "submit_button": "Submit",
    "success_message": "Your submission was received",
    "error_message": "Please try again later"
}

@router.get("/localized")
async def get_localized_content(
    request: Request,
    lang: str = Query('en', regex="^(en|sw|fr)$"),
    translator: UITranslator = Depends()
):
    """Get all UI content in specified language"""
    return {
        key: translator.get_translation(value, lang)
        for key, value in BASE_CONTENT.items()
    }

@router.get("/string/{msg_id}")
async def get_single_string(
    msg_id: str,
    lang: str = Query('en'),
    translator: UITranslator = Depends()
):
    """Get specific translation string"""
    if msg_id not in BASE_CONTENT:
        raise HTTPException(status_code=404, detail="Message ID not found")
    
    return {
        "id": msg_id,
        "translation": translator.get_translation(BASE_CONTENT[msg_id], lang)
    }