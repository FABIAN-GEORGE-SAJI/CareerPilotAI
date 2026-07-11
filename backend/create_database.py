from app.database.base import Base
from app.database.database import engine

# Import all models so SQLAlchemy registers them
import app.models

print("Creating database...")

Base.metadata.create_all(bind=engine)

print("Database created successfully!")