from pydantic import BaseModel

from app.schemas.resume_data import ResumeData


class ResumeUploadResponse(BaseModel):
    message: str
    filename: str
    resume: ResumeData