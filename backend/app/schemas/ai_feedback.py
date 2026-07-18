from pydantic import BaseModel, Field


class AIFeedback(BaseModel):

    strengths: list[str] = Field(default_factory=list)

    weaknesses: list[str] = Field(default_factory=list)

    high_priority_actions: list[str] = Field(default_factory=list)

    low_priority_actions: list[str] = Field(default_factory=list)

    missing_keywords: list[str] = Field(default_factory=list)

    overall_feedback: str = ""

    hiring_readiness: str = ""