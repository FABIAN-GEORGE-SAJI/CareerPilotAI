from pydantic import BaseModel

from app.schemas.job_data import JobDescriptionData


class JobUploadResponse(BaseModel):
    message: str
    job: JobDescriptionData