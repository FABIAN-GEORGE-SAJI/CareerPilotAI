from pydantic import BaseModel

from app.schemas.similarity_level import SimilarityLevel


class SkillMatch(BaseModel):
    """
    Final ATS decision for one job skill.
    """

    resume_skill: str = ""

    job_skill: str

    matched: bool

    exact: bool

    similarity: float = 0.0

    relationship: SimilarityLevel = SimilarityLevel.NONE

    weight: float = 0.0