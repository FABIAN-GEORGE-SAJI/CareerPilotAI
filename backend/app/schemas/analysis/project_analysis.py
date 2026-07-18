from pydantic import BaseModel


class ProjectAnalysis(BaseModel):
    """Projects analysis from resume."""

    overall_score: float = 0.0
