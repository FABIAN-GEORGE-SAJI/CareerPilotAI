from pydantic import BaseModel


class CareerAgentRequest(BaseModel):
    resume_id: int
    job_id: int
    message: str


class CareerAgentResponse(BaseModel):
    response: str