from pydantic import BaseModel, Field


class AIJob(BaseModel):

    title: str = ""

    company: str = ""

    summary: str = ""

    skills: list[str] = Field(default_factory=list)

    required_skills: list[str] = Field(default_factory=list)

    preferred_skills: list[str] = Field(default_factory=list)

    soft_skills: list[str] = Field(default_factory=list)

    responsibilities: list[str] = Field(default_factory=list)

    qualifications: list[str] = Field(default_factory=list)

    location: str = ""

    employment_type: str = ""