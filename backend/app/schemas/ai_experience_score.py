from pydantic import BaseModel


class AIExperienceScore(BaseModel):

    score: float = 0.0

    reason: str = ""