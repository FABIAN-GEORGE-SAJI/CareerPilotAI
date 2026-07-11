from pathlib import Path

from sqlalchemy import create_engine


# backend/
BASE_DIR = Path(__file__).resolve().parents[2]

# backend/data/
DATA_DIR = BASE_DIR / "data"

# Create the directory if it doesn't exist
DATA_DIR.mkdir(parents=True, exist_ok=True)

# SQLite database file
DATABASE_URL = f"sqlite:///{DATA_DIR / 'careerpilot.db'}"

# SQLAlchemy engine
engine = create_engine(
    DATABASE_URL,
    echo=True,
)