from pathlib import Path
import os

from sqlalchemy import create_engine

from app.database.base import Base
import app.models  # noqa: F401


DB_PATH = os.getenv("DATABASE_PATH", "data/careerpilot.db")

Path(DB_PATH).parent.mkdir(parents=True, exist_ok=True)

DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)


def init_db():
    """
    Single canonical create_all() entry point.

    Creates all tables registered on the canonical `app.database.base.Base`
    metadata.
    """
    Base.metadata.create_all(bind=engine)