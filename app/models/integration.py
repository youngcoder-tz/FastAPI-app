class ThirdPartyIntegration(TimeStampedBase):
    __tablename__ = "third_party_integrations"
    
    id = Column(UUID, primary_key=True)
    user_id = Column(UUID, ForeignKey("users.id"))
    service_name = Column(String(100))
    service_user_id = Column(String(100))
    connected_at = Column(DateTime)
    last_synced_at = Column(DateTime)