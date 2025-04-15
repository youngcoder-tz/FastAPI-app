from celery import shared_task
from app.services.ai import categorize_text

@shared_task
def categorize_complaint(complaint_id: str):
    with get_db_session() as db:
        complaint = db.query(Complaint).get(complaint_id)
        if complaint:
            categories = categorize_text(complaint.description)
            complaint.tags = categories
            db.commit()