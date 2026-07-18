from typing import Any

from pydantic import BaseModel, Field

from app.schemas.analysis.master_analysis import MasterAnalysis
from app.schemas.ai_ats_validation import AISkillEvidence


class ATSResult(BaseModel):

    ats_score: float = 0.0

    overall_score: float = 0.0

    skill_score: float = 0.0

    required_skill_score: float = 0.0

    preferred_skill_score: float = 0.0

    soft_skill_score: float = 0.0

    education_score: float = 0.0

    experience_score: float = 0.0

    experience_reason: str = ""

    project_score: float = 0.0

    semantic_score: float = 0.0

    keyword_coverage: float = 0.0

    score_adjustment: float = 0.0

    matched_skills: list[str] = Field(default_factory=list)

    missing_skills: list[str] = Field(default_factory=list)

    recommendations: list[str] = Field(default_factory=list)

    # Recruiter verdict, surfaced on the ATS page as the "AI Executive
    # Verdict" banner.
    hire: bool = False

    hire_reason: str = ""

    confidence: float = 0.0

    strengths: list[str] = Field(default_factory=list)

    weaknesses: list[str] = Field(default_factory=list)

    # Per-skill proof behind each entry in matched_skills - lets the UI show
    # *why* a skill was credited instead of just asserting that it was.
    skill_evidence: list[AISkillEvidence] = Field(default_factory=list)

    ai_validation: dict[str, Any] = Field(default_factory=dict)

    analysis: MasterAnalysis = Field(default_factory=MasterAnalysis)
