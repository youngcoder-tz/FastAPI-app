class CitizenFeedback(TimeStampedBase):
    __tablename__ = "citizen_feedback"
    
    id = Column(UUID(as_uuid=True), primary_key=True)
    complaint_id = Column(UUID(as_uuid=True), ForeignKey("complaints.id"))
    rating = Column(Integer)  # 1-5 scale
    comments = Column(Text)
    is_anonymous = Column(Boolean, default=True)
    response_time_rating = Column(Integer)  # 1-5 scale
    resolution_rating = Column(Integer)  # 1-5 scale