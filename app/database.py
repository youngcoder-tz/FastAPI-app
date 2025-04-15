# app/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings

# Access DATABASE_URL from settings
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Add after engine creation
def create_extensions(connection):
    connection.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')
    connection.execute('CREATE EXTENSION IF NOT EXISTS "pgcrypto"')
    connection.execute('CREATE EXTENSION IF NOT EXISTS "pg_trgm"')

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()