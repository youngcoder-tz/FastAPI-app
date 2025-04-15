from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.complaint import Complaint
from app.schemas.complaint import ComplaintCreate, ComplaintUpdate, Complaint
from app.auth.dependencies import get_current_user
from app.ws import manager
import json
from sqlalchemy.dialects.postgresql import UUID 
from app.services.escalation import EscalationEngine
from uuid import UUID
from app.services.voice import VoiceProcessor
from app.services.language import LanguageProcessor

# Temporary dummy event producer (replace with your actual implementation)
class DummyProducer:
    async def publish(self, topic, message):
        print(f"[Event Published] Topic: {topic}, Message: {message}")

event_producer = DummyProducer()
from uuid import UUID

router = APIRouter(prefix="/complaints", tags=["complaints"])

@router.post("/voice-complaint")
async def create_voice_complaint(
    audio: UploadFile = File(...),
    voice: VoiceProcessor = Depends(),
    lang: LanguageProcessor = Depends()
):
    # Process voice
    voice_result = await voice.process_voice_message(audio)
    
    # Detect and translate if needed
    if lang.detect(voice_result['text']) != 'en':
        translated = await translate_text(voice_result['text'])
    
    # Save to database
    complaint = Complaint(
        description=translated or voice_result['text'],
        original_content=voice_result['text'],
        is_voice_submission=True
    )

@router.post("/", response_model=Complaint)
def create_complaint(
    complaint: ComplaintCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    db_complaint = Complaint(
        **complaint.dict(),
        citizen_id=current_user["sub"],
        status="pending"
    )
    db.add(db_complaint)
    db.commit()
    db.refresh(db_complaint)
    return db_complaint

@router.patch("/{complaint_id}", response_model=Complaint)
async def update_complaint(
    complaint_id: str,
    update_data: ComplaintUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    complaint = db.query(Complaint).filter(Complaint.id == complaint_id).first()
    if not complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")
    
    # Update complaint
    for field, value in update_data.dict(exclude_unset=True).items():
        setattr(complaint, field, value)
    
    db.commit()
    db.refresh(complaint)
    
    # Notify citizen via WebSocket
    await manager.send_personal_message(
        json.dumps({
            "event": "complaint_updated",
            "data": {
                "complaint_id": str(complaint.id),
                "new_status": complaint.status
            }
        }),
        str(complaint.citizen_id)
    )
    
    return complaint



@router.post("/{complaint_id}/auto-assign")
async def auto_assign_complaint(
    complaint_id: UUID,
    db: Session = Depends(get_db),
    escalation: EscalationEngine = Depends()
):
    complaint = db.query(Complaint).get(complaint_id)
    
    # Determine optimal assignee
    level = escalation.determine_escalation(complaint)
    assignee = find_available_officer(level, complaint.location)
    
    # Update and notify
    complaint.assigned_to = assignee.id
    complaint.escalation_level = level
    
    # Real-time update
    await event_producer.publish("assignments", {
        "complaint_id": str(complaint.id),
        "assigned_to": str(assignee.id),
        "escalation_level": level.name
    })
    
    db.commit()
    return {"message": f"Escalated to {level.name}"}