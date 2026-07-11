from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

# Project root (CareerPilotAI/)
BASE_DIR = Path(__file__).resolve().parents[3]


class Settings(BaseSettings):
    """
    Central configuration for CareerPilot AI.
    """

    APP_NAME: str = "CareerPilot AI"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    DATA_DIR: Path = BASE_DIR / "backend" / "data"
    RESUME_DIR: Path = DATA_DIR / "resumes"
    JOB_DESCRIPTION_DIR: Path = DATA_DIR / "job_descriptions"
    CHROMA_DIR: Path = DATA_DIR / "chroma"
    TEMP_DIR: Path = DATA_DIR / "temp"

    MAX_UPLOAD_SIZE_MB: int = 10

    ALLOWED_EXTENSIONS: list[str] = Field(
        default_factory=lambda: [".pdf", ".docx"]
    )

    # AI Configuration
    GEMINI_API_KEY: str = ""

    GEMINI_MODEL: str = "gemini-2.5-flash"

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
    )


settings = Settings()