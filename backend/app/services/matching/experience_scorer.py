from app.schemas.ai_experience_score import AIExperienceScore
from app.schemas.job_data import JobDescriptionData
from app.schemas.resume_data import ResumeData

from app.services.ai.gemini_service import GeminiService
from app.services.matching.base_scorer import BaseScorer


class ExperienceScorer(BaseScorer):
    """
    AI-powered experience scorer.
    """

    def __init__(self):
        self.ai = GeminiService()

    async def score(
        self,
        resume: ResumeData,
        job: JobDescriptionData,
    ) -> AIExperienceScore:

        if not resume.experience:
            return AIExperienceScore(
                score=0,
                reason="No professional experience found in the resume.",
            )

        return await self.ai.score_experience(
            resume,
            job,
        )