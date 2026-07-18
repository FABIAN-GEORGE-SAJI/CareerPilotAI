from pydantic import BaseModel


class OverallAnalysis(BaseModel):
    """Overall resume analysis and scores."""

    overall_score: float = 0.0
