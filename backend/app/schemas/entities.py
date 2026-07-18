from pydantic import BaseModel


class Education(BaseModel):

    degree: str = ""

    specialization: str = ""

    institution: str = ""

    graduation_year: str = ""

    cgpa: str = ""


class Experience(BaseModel):

    company: str = ""

    position: str = ""

    start_date: str = ""

    end_date: str = ""

    description: list[str] = []


class Project(BaseModel):

    title: str = ""

    technologies: list[str] = []

    description: list[str] = []


class Certification(BaseModel):

    name: str = ""

    issuer: str = ""

    issue_date: str = ""

    expiry_date: str = ""