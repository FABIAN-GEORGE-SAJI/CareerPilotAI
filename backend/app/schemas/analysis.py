from pydantic import BaseModel, Field
from typing import List

class SkillEvaluation(BaseModel):
    skill_name: str = Field(description="The name of the explicit or contextually implied skill.")
    type: str = Field(description="Must be either 'explicit' (written directly) or 'implicit' (inferred from actions).")
    evidence: str = Field(description="Direct quotation or clear action phrase from the resume that proves this proficiency.")

class SectionScore(BaseModel):
    score: float = Field(description="Calculated score out of 100.")
    status: str = Field(description="Excellent Match, Strong Match, Moderate Match, Weak Match, or Poor Match.")
    findings: List[str] = Field(description="Concrete textual facts justifying this score.")
    implied_gaps: List[str] = Field(description="Critical missing proficiencies or cross-domain missing links.")

class UniversalATSReport(BaseModel):
    overall_score: float
    skill_score: float
    education_score: float
    experience_score: float
    project_score: float
    semantic_score: float
    soft_skill_score: float
    keyword_coverage: float
    
    matched_skills: List[str] = Field(description="List of skills verified through text or valid deduction.")
    missing_skills: List[str] = Field(description="Crucial skills explicitly required by the job but completely unsupported by text or implication.")
    
    strengths: List[str] = Field(description="Citations of high-impact accomplishments matching the role's needs.")
    weaknesses: List[str] = Field(description="Specific structural gaps or lack of scope depth.")
    recommendations: List[str] = Field(description="Actionable blueprint detailing exactly what to add to the resume to align with this target role.")