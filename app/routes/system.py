@router.get("/system/status")
async def system_status(db: Session = Depends(get_db)):
    return {
        "database": "active" if db.execute(text("SELECT 1")).scalar() else "inactive",
        "migrations": get_alembic_version()
    }