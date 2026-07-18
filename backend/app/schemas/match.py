from pydantic import BaseModel

from app.schemas.ats_result import ATSResult


class MatchRequest(BaseModel):
    resume_id: int
    job_id: int


class MatchResponse(BaseModel):
    report: ATSResult