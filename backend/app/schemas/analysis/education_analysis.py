from pydantic import BaseModel


class EducationAnalysis(BaseModel):
    """Education section analysis."""

    score: float = 0.0
