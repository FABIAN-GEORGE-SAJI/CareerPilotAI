import asyncio

from app.schemas.ats_result import ATSResult
from app.schemas.job_data import JobDescriptionData
from app.schemas.resume_data import ResumeData

from app.services.matching.skill_scorer import SkillScorer
from app.services.matching.education_scorer import EducationScorer
from app.services.matching.project_scorer import ProjectScorer
from app.services.matching.experience_scorer import ExperienceScorer

from app.services.matching.score_calculator import ScoreCalculator
from app.services.matching.recommendation_engine import RecommendationEngine


class ATSScorer:
    """
    Coordinates all scoring modules and produces
    the final ATS report.
    """

    def __init__(self):

        self.skill_scorer = SkillScorer()

        self.education_scorer = EducationScorer()

        self.project_scorer = ProjectScorer()

        self.experience_scorer = ExperienceScorer()

    async def score(
        self,
        resume: ResumeData,
        job: JobDescriptionData,
    ) -> ATSResult:

        # ----------------------------------------
        # Run all scorers concurrently
        # ----------------------------------------
        (
            skill_result,
            education_score,
            project_score,
            experience_result,
        ) = await asyncio.gather(

            self.skill_scorer.score(
                resume,
                job,
            ),

            self.education_scorer.score(
                resume,
                job,
            ),

            self.project_scorer.score(
                resume,
                job,
            ),

            self.experience_scorer.score(
                resume,
                job,
            ),
        )

        # ----------------------------------------
        # Unpack Skill Result
        # ----------------------------------------
        (
            skill_score,
            required_skill_score,
            preferred_skill_score,
            soft_skill_score,
            matched_skills,
            missing_skills,
        ) = skill_result

        experience_score = experience_result.score

        # ----------------------------------------
        # Calculate Overall Score
        # ----------------------------------------
        overall_score = ScoreCalculator.calculate(
            skill_score,
            education_score,
            project_score,
            experience_score,
        )

        # ----------------------------------------
        # Build Report
        # ----------------------------------------
        report = ATSResult(

            overall_score=overall_score,

            skill_score=skill_score,

            required_skill_score=required_skill_score,

            preferred_skill_score=preferred_skill_score,

            soft_skill_score=soft_skill_score,

            education_score=education_score,

            project_score=project_score,

            experience_score=experience_score,

            experience_reason=experience_result.reason,

            matched_skills=matched_skills,

            missing_skills=missing_skills,
        )

        # ----------------------------------------
        # Generate Recommendations
        # ----------------------------------------
        report.recommendations = RecommendationEngine.generate(
            report,
        )

        return report