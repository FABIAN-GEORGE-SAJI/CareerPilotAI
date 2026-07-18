from pydantic import BaseModel
from app.schemas.entities import (
    Education,
    Experience,
    Project,
    Certification,
)

class BasicInfo(BaseModel):
    name: str = ""
    email: str = ""
    phone: str = ""


class ResumeData(BaseModel):
    basic_info: BasicInfo

    sections: dict[str, list[str]] = {}

    skills: list[str] = []

    education: list[Education] = []

    experience: list[Experience] = []

    projects: list[Project] = []

    certifications: list[Certification] = []
    
    languages: list[str] = []

    summary: str = ""