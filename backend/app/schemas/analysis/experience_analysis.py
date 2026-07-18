from pydantic import BaseModel


class ExperienceAnalysis(BaseModel):
    """Experience section analysis."""

    score: float = 0.0

    # Populated from AIATSValidation.experience_reason by ATSScorer. Read by
    # the ATS page's "Experience Compatibility Analysis" panel
    # (report.analysis.experience.reason) - without this field, ATSScorer's
    # assignment to it raises, since Pydantic v2 rejects sets to undeclared
    # attributes.
    reason: str = ""
