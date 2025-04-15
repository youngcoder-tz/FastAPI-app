from enum import Enum as PyEnum

class EventType(PyEnum):
    COMPLAINT_UPDATE = "complaint_updated"
    PROMISE_VERIFIED = "promise_verified"
    NEW_ASSIGNMENT = "new_assignment"

class Notification(TimeStampedBase):
    __tablename__ = "notifications"
    
    id = Column(UUID(as_uuid=True), primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    event_type = Column(Enum(EventType))
    message = Column(JSONB)  # Structured event data
    is_read = Column(Boolean, default=False)
    expires_at = Column(DateTime)