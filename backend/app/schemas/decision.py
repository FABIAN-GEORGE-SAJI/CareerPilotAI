from pydantic import BaseModel

from app.schemas.similarity_level import SimilarityLevel


class Decision(BaseModel):
    """
    Final decision produced by the matching policy.
    """

    accepted: bool

    relationship: SimilarityLevel

    weight: float

    confidence: float

    reasons: list[str]