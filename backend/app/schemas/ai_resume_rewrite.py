from pydantic import BaseModel, Field


class AIExperienceRewrite(BaseModel):
    company: str = ""
    role: str = ""
    rewritten_description: str = ""


class AIProjectRewrite(BaseModel):
    name: str = ""
    rewritten_description: str = ""


class AIResumeRewrite(BaseModel):

    professional_summary: str = ""

    improved_skills: list[str] = Field(default_factory=list)

    improved_experience: list[AIExperienceRewrite] = Field(
        default_factory=list
    )

    improved_projects: list[AIProjectRewrite] = Field(
        default_factory=list
    )

    added_keywords: list[str] = Field(default_factory=list)

    additional_recommendations: list[str] = Field(
        default_factory=list
    )