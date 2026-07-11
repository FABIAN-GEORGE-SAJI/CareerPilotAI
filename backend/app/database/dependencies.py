from collections.abc import Generator

from sqlalchemy.orm import Session

from app.database.session import SessionLocal


def get_session() -> Generator[Session, None, None]:
    """
    Creates a database session and ensures it is closed properly.
    """

    session = SessionLocal()

    try:
        yield session

    finally:
        session.close()