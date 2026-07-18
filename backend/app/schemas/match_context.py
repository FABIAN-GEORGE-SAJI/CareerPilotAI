from pydantic import BaseModel

from app.schemas.resume_data import ResumeData
from app.schemas.job_data import JobDescriptionData
from app.schemas.ats_result import ATSResult


class MatchContext(BaseModel):

    resume: ResumeData

    job: JobDescriptionData

    report: ATSResult