from sqlalchemy import create_engine

from app.database.base import Base
import app.models  # noqa: F401  (registers ORM models on Base.metadata)

DATABASE_URL = "sqlite:///./data/careerpilot.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})


def init_db() -> None:
    """
    Single canonical create_all() entry point.

    Creates all tables registered on the canonical `app.database.base.Base`
    metadata (i.e. everything under app/models). Safe to call multiple times;
    SQLAlchemy only creates tables that don't already exist.
    """
    Base.metadata.create_all(bind=engine)
