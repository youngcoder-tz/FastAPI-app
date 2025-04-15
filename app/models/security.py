from sqlalchemy import Column, String, Boolean, Enum ,ForeignKey


class SecurityLog(TimeStampedBase):
    __tablename__ = "security_logs"
    
    id = Column(UUID, primary_key=True)
    user_id = Column(UUID, ForeignKey("users.id"))
    ip_address = Column(String(45))
    action_type = Column(Enum(
        'token_generated',
        'journalist_verified',
        'complaint_filed',
        'promise_updated'
    ))
    status = Column(Enum('success', 'failed'))