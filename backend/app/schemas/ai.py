from pydantic import BaseModel


class AIRequest(BaseModel):

    resume_id: int

    job_id: int