from sqlalchemy import Index
from app.models import Complaint, CampaignPromise

def create_indexes():
    # Complaint query optimization
    Index('idx_complaint_status', Complaint.status)
    Index('idx_complaint_citizen', Complaint.citizen_id)
    
    # Campaign promise optimization
    Index('idx_promise_politician', CampaignPromise.politician_id)
    Index('idx_promise_status', CampaignPromise.status)