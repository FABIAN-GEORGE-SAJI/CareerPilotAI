from pydantic import BaseModel, Field

from app.schemas.analysis.ats_validation import ATSValidation
from app.schemas.analysis.education_analysis import EducationAnalysis
from app.schemas.analysis.experience_analysis import ExperienceAnalysis
from app.schemas.analysis.improvement_analysis import ImprovementAnalysis
from app.schemas.analysis.overall_analysis import OverallAnalysis
from app.schemas.analysis.project_analysis import ProjectAnalysis
from app.schemas.analysis.recommendation import Recommendation
from app.schemas.analysis.recruiter_analysis import RecruiterAnalysis
from app.schemas.analysis.semantic_analysis import SemanticAnalysis
from app.schemas.analysis.skill_analysis import SkillAnalysis


class MasterAnalysis(BaseModel):
    """
    Internal analysis object shared by all AI modules.
    """

    overall: OverallAnalysis = Field(default_factory=OverallAnalysis)
    skills: SkillAnalysis = Field(default_factory=SkillAnalysis)
    experience: ExperienceAnalysis = Field(default_factory=ExperienceAnalysis)
    projects: ProjectAnalysis = Field(default_factory=ProjectAnalysis)
    education: EducationAnalysis = Field(default_factory=EducationAnalysis)
    semantic: SemanticAnalysis = Field(default_factory=SemanticAnalysis)
    recommendations: Recommendation = Field(default_factory=Recommendation)
    recruiter: RecruiterAnalysis = Field(default_factory=RecruiterAnalysis)
    ats_validation: ATSValidation = Field(default_factory=ATSValidation)
    improvements: ImprovementAnalysis = Field(default_factory=ImprovementAnalysis)
