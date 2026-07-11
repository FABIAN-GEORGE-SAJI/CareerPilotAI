from pydantic import BaseModel, Field

from app.schemas.semantic_match_result import SemanticSkillMatch


class HybridMatchResult(BaseModel):
    """
    Final result returned by the HybridMatcher.
    """

    matched: list[SemanticSkillMatch] = Field(default_factory=list)

    missing: list[str] = Field(default_factory=list)

    score: float = 0.0