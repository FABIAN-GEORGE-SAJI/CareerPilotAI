from pydantic import BaseModel, Field


class AISectionScores(BaseModel):
    """Per-dimension ATS sub-scores, judged with full profile context."""

    skills: float = 0.0
    required_skills: float = 0.0
    preferred_skills: float = 0.0
    soft_skills: float = 0.0
    education: float = 0.0
    experience: float = 0.0
    projects: float = 0.0
    semantic: float = 0.0


class AISkillEvidence(BaseModel):
    """
    A single matched skill together with the proof Gemini used to credit it.

    ``evidence_type`` distinguishes a skill the candidate stated outright
    (e.g. it appears in their skills list) from one that was only inferred
    from surrounding context (e.g. "built a CI/CD pipeline" implying
    familiarity with automated deployment tooling).
    """

    skill: str = ""
    evidence_type: str = "explicit"  # "explicit" or "implicit"
    evidence: str = ""


class AIATSValidation(BaseModel):
    """
    Structured response contract for the ``ats_validator`` prompt.

    This is the raw shape Gemini is asked to return. ``ATSScorer`` maps it
    onto the persisted ``ATSResult`` - keeping the two separate lets the AI
    contract evolve (new fields, renamed fields) without having to touch the
    database-facing report shape in lockstep.
    """

    final_score: float = 0.0
    score_adjustment: float = 0.0

    matched_skills: list[str] = Field(default_factory=list)
    missing_skills: list[str] = Field(default_factory=list)
    recommendations: list[str] = Field(default_factory=list)

    hire: bool = False
    hire_reason: str = ""
    confidence: float = 0.0

    strengths: list[str] = Field(default_factory=list)
    weaknesses: list[str] = Field(default_factory=list)

    experience_reason: str = ""
    keyword_coverage: float = 0.0

    section_scores: AISectionScores = Field(default_factory=AISectionScores)
    skill_evidence: list[AISkillEvidence] = Field(default_factory=list)

