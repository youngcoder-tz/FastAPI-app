@shared_task
def process_event(event_data: dict):
    with get_db_session() as db:
        # Store in database
        notification = Notification(
            user_id=event_data["user_id"],
            event_type=event_data["type"],
            message=event_data["payload"],
            expires_at=datetime.utcnow() + timedelta(days=30)
        )
        db.add(notification)
        db.commit()
        
        # Push to connected clients
        channel = "complaints" if "complaint" in event_data["type"] else "promises"
        asyncio.run(
            ws_manager.send_personal(
                event_data["user_id"],
                event_data,
                channel
            )
        )