from sqlalchemy import Column, String, Boolean, Enum ,ForeignKey , UUID



class AdminLog(TimeStampedBase):
    __tablename__ = "admin_logs"
    
    id = Column(UUID, primary_key=True)
    admin_id = Column(UUID, ForeignKey("users.id"))
    action = Column(String(255))
    target_id = Column(UUID)  # Polymorphic FK
    description = Column(Text)

class AIModelConfig(TimeStampedBase):
    __tablename__ = "ai_model_configs"
    
    id = Column(UUID, primary_key=True)
    feature_name = Column(String(100))
    configuration = Column(JSON) 