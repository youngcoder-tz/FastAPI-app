def seed_initial_roles(db):
    from app.models.user import User
    # Create system admin if not exists
    if not db.query(User).filter(User.role == 'admin').first():
        admin = User(
            email="admin@wajibika.tz",
            hashed_password=hash_password("SecureAdminPass123!"),
            role="admin",
            is_verified=True
        )
        db.add(admin)
        db.commit()