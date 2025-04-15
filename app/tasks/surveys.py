@shared_task
def send_resolution_surveys():
    """Trigger feedback requests after complaint resolution"""
    with get_db_session() as db:
        resolved = db.query(Complaint).filter(
            Complaint.status == "resolved",
            Complaint.resolved_at >= datetime.now() - timedelta(days=3),
            ~exists().where(CitizenFeedback.complaint_id == Complaint.id)
        ).all()
        
        for complaint in resolved:
            send_survey_email(
                recipient=complaint.citizen.email,
                complaint_id=complaint.id,
                survey_link=generate_survey_link(complaint)
            )
            create_reminder_task(complaint.id)