from sqlalchemy import Column, Integer, Date

class ComplaintForecast(TimeStampedBase):
    __tablename__ = "complaint_forecasts"
    
    id = Column(UUID(as_uuid=True), primary_key=True)
    date = Column(Date, index=True)
    predicted_count = Column(Integer)
    actual_count = Column(Integer, nullable=True)
    confidence_interval = Column(JSONB)  # {upper: 120, lower: 80}
    model_version = Column(String(50))