from pydantic import BaseModel, Field
from app.schemas.similarity_level import SimilarityLevel

class SemanticSkillMatch(BaseModel):

    resume_skill: str

    job_skill: str

    similarity: float

    relationship: SimilarityLevel = SimilarityLevel.NONE

    weight: float = 0.0


class SemanticMatchResult(BaseModel):
    """
    Result returned by SemanticMatcher.
    """

    matched: list[SemanticSkillMatch] = Field(default_factory=list)

    unmatched: list[str] = Field(default_factory=list)

    average_similarity: float = 0.0