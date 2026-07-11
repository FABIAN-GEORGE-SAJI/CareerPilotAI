from pydantic import BaseModel

from app.schemas.resume_data import ResumeData
from app.schemas.job_data import JobDescriptionData
from app.schemas.ats_result import ATSResult


class MatchRequest(BaseModel):
    resume_id: int
    job_id: int


class MatchResponse(BaseModel):
    report: ATSResult