from pydantic import BaseModel


class SkillEvidence(BaseModel):
    """
    Evidence collected before making
    the ATS matching decision.
    """

    resume_skill: str = ""

    job_skill: str

    exact: bool = False

    similarity: float = 0.0