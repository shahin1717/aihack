from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.config import get_settings

settings = get_settings()

# MySQL engine
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,    # prevents stale connections
    pool_recycle=3600,     # refreshes connection every hour
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
