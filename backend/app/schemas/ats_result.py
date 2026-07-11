from pydantic import BaseModel, Field


class ATSResult(BaseModel):

    overall_score: float = 0.0

    skill_score: float = 0.0

    required_skill_score: float = 0.0

    preferred_skill_score: float = 0.0

    soft_skill_score: float = 0.0

    education_score: float = 0.0

    experience_score: float = 0.0

    experience_reason: str = ""

    project_score: float = 0.0

    semantic_score: float = 0.0

    matched_skills: list[str] = Field(default_factory=list)

    missing_skills: list[str] = Field(default_factory=list)

    recommendations: list[str] = Field(default_factory=list)