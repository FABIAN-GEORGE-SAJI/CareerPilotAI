from pydantic import BaseModel, Field


class AIEducation(BaseModel):
    degree: str = ""
    institution: str = ""
    year: str = ""


class AIExperience(BaseModel):
    title: str = ""
    company: str = ""
    duration: str = ""

    description: list[str] = Field(default_factory=list)


class AIProject(BaseModel):
    name: str = ""

    technologies: list[str] = Field(default_factory=list)

    description: list[str] = Field(default_factory=list)


class AICertification(BaseModel):
    name: str = ""
    issuer: str = ""


class AIBasicInfo(BaseModel):
    name: str = ""
    email: str = ""
    phone: str = ""


class AIResume(BaseModel):

    basic_info: AIBasicInfo

    skills: list[str] = Field(default_factory=list)

    education: list[AIEducation] = Field(default_factory=list)

    experience: list[AIExperience] = Field(default_factory=list)

    projects: list[AIProject] = Field(default_factory=list)

    certifications: list[AICertification] = Field(default_factory=list)

    languages: list[str] = Field(default_factory=list)

    summary: str = ""