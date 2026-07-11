from pydantic import BaseModel, Field


class MatchResult(BaseModel):
    """
    Result returned by the matching pipeline.
    """

    matched: list[str] = Field(default_factory=list)

    missing: list[str] = Field(default_factory=list)

    score: float = 0.0

    confidence: float = 1.0

    normalized_resume: set[str] = Field(default_factory=set)

    normalized_job: set[str] = Field(default_factory=set)