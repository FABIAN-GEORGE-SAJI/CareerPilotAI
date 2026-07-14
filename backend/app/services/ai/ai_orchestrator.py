from app.schemas.ai_cover_letter import AICoverLetter
from app.schemas.ai_feedback import AIFeedback
from app.schemas.ai_interview_questions import AIInterviewQuestions
from app.schemas.ai_learning_roadmap import AILearningRoadmap
from app.schemas.ai_resume_rewrite import AIResumeRewrite

from app.services.ai.gemini_service import GeminiService
from app.services.matching.matching_service import MatchingService


class AIOrchestrator:

    def __init__(self):

        self.matching = MatchingService()

        self.gemini = GeminiService()

    async def generate_feedback(
        self,
        resume_id: int,
        job_id: int,
    ) -> AIFeedback:

        context = await self.matching.build_context(
            resume_id,
            job_id,
        )

        return await self.gemini.generate_feedback(
            context.report,
        )

    async def generate_cover_letter(
        self,
        resume_id: int,
        job_id: int,
    ) -> AICoverLetter:

        context = await self.matching.build_context(
            resume_id,
            job_id,
        )

        return await self.gemini.generate_cover_letter(
            context.resume,
            context.job,
        )

    async def rewrite_resume(
        self,
        resume_id: int,
        job_id: int,
    ) -> AIResumeRewrite:

        context = await self.matching.build_context(
            resume_id,
            job_id,
        )

        return await self.gemini.rewrite_resume(
            context.resume,
            context.job,
        )

    async def generate_interview_questions(
        self,
        resume_id: int,
        job_id: int,
    ) -> AIInterviewQuestions:

        context = await self.matching.build_context(
            resume_id,
            job_id,
        )

        return await self.gemini.generate_interview_questions(
            context.resume,
            context.job,
        )

    async def generate_learning_roadmap(
        self,
        resume_id: int,
        job_id: int,
    ) -> AILearningRoadmap:

        context = await self.matching.build_context(
            resume_id,
            job_id,
        )

        return await self.gemini.generate_learning_roadmap(
            context.resume,
            context.job,
            context.report,
        )