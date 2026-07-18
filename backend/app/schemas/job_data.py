from pydantic import BaseModel


class JobDescriptionData(BaseModel):

    title: str = ""

    company: str = ""

    summary: str = ""

    skills: list[str] = []

    required_skills: list[str] = []

    preferred_skills: list[str] = []

    soft_skills: list[str] = []

    responsibilities: list[str] = []

    qualifications: list[str] = []

    location: str = ""

    employment_type: str = ""

    experience: str = ""

    education: str = ""

    keywords: list[str] = []