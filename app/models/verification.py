from app.models.base import TimeStampedBase

class JournalistVerification(TimeStampedBase):
    __tablename__ = "journalist_verifications"
    
    id = Column(UUID, primary_key=True)
    user_id = Column(UUID, ForeignKey("users.id"))
    social_media_id_url = Column(String(255))
    verified_by_admin = Column(Boolean, default=False)
    verification_date = Column(DateTime)