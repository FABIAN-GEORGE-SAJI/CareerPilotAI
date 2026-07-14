import json

from google import genai
import asyncio

from google.genai.errors import (
    ServerError,
    ClientError,
)

from app.core.config import settings
from app.core.logging import logger


from app.schemas.ai_cover_letter import AICoverLetter
from app.schemas.ai_experience_score import AIExperienceScore
from app.schemas.ai_feedback import AIFeedback
from app.schemas.ai_job import AIJob
from app.schemas.ai_resume import AIResume
from app.schemas.ai_resume_rewrite import AIResumeRewrite
from app.schemas.ats_result import ATSResult
from app.schemas.job_data import JobDescriptionData
from app.schemas.resume_data import ResumeData
from app.schemas.ai_interview_questions import AIInterviewQuestions
from app.schemas.ai_learning_roadmap import AILearningRoadmap

from app.services.ai.base import AIService

from app.services.mapping.feedback_mapper import FeedbackMapper
from app.services.mapping.job_mapper import JobMapper
from app.services.mapping.resume_mapper import ResumeMapper

from app.utils.json_parser import JSONParser
from app.utils.prompt_loader import PromptLoader


class GeminiService(AIService):

    def __init__(self):

        self.client = genai.Client(
            api_key=settings.GEMINI_API_KEY,
        )

        self.model = settings.GEMINI_MODEL

    
    @staticmethod
    def _debug_output(
        title: str,
        content: str,
    ) -> None:

        logger.info("=" * 80)
        logger.info(title)
        logger.info("=" * 80)
        logger.info(content)
        logger.info("=" * 80)

    
    async def _generate_json(
        self,
        prompt_name: str,
        payload: dict,
        title: str,
    ) -> dict:

        prompt = PromptLoader.load(
            prompt_name,
        )

        full_prompt = "\n\n".join([
            prompt,
            json.dumps(
                payload,
                indent=2,
                ensure_ascii=False,
            ),
        ])

        response = await self.generate_text(
            full_prompt,
        )

        self._debug_output(
            title,
            response,
        )

        return JSONParser.parse(
            response,
        )
    
    async def _generate_from_text(
        self,
        prompt_name: str,
        label: str,
        text: str,
        title: str,
    ) -> dict:

        prompt = PromptLoader.load(
            prompt_name,
        )

        full_prompt = "\n\n".join([
            prompt,
            f"{label}:",
            text,
        ])

        response = await self.generate_text(
            full_prompt,
        )

        self._debug_output(
            title,
            response,
        )

        return JSONParser.parse(
            response,
        )

    async def generate_text(
        self,
        prompt: str,
    ) -> str:

        for attempt in range(3):

            try:

                response = self.client.models.generate_content(
                    model=self.model,
                    contents=prompt,
                )

                return response.text.strip()

            except ServerError:

                if attempt == 2:
                    raise

                await asyncio.sleep(2 ** attempt)

            except ClientError:
                raise

    async def parse_resume(
        self,
        text: str,
    ) -> ResumeData:

        data = await self._generate_from_text(
            prompt_name="resume_parser",
            label="Resume",
            text=text,
            title="RAW GEMINI RESUME RESPONSE",
        )

        ai_resume = AIResume(
            **data,
        )

        return ResumeMapper.to_resume_data(
            ai_resume,
        )

    async def parse_job(
        self,
        text: str,
    ) -> JobDescriptionData:

        data = await self._generate_from_text(
            prompt_name="job_parser",
            label="Job Description",
            text=text,
            title="RAW GEMINI JOB RESPONSE",
        )

        ai_job = AIJob(
            **data,
        )

        return JobMapper.to_job_data(
            ai_job,
        )

    async def score_experience(
        self,
        resume: ResumeData,
        job: JobDescriptionData,
    ) -> AIExperienceScore:

        payload = {
            "resume_experience": [
                experience.model_dump()
                for experience in resume.experience
            ],
            "job": job.model_dump(),
        }

        data = await self._generate_json(
            prompt_name="experience_score",
            payload=payload,
            title="RAW EXPERIENCE SCORE",
        )

        return AIExperienceScore(
            **data,
        )
    async def generate_feedback(
        self,
        report: ATSResult,
    ) -> AIFeedback:

        data = await self._generate_json(
            prompt_name="feedback_generator",
            payload=report.model_dump(),
            title="RAW FEEDBACK",
        )

        feedback = AIFeedback(
            **data,
        )

        return FeedbackMapper.to_feedback(
            feedback,
        )

    async def rewrite_resume(
        self,
        resume: ResumeData,
        job: JobDescriptionData,
    ) -> AIResumeRewrite:

        payload = {
            "resume": resume.model_dump(),
            "job": job.model_dump(),
        }

        data = await self._generate_json(
            prompt_name="resume_rewrite",
            payload=payload,
            title="RAW RESUME REWRITE",
        )

        return AIResumeRewrite(
            **data,
        )

    async def generate_cover_letter(
        self,
        resume: ResumeData,
        job: JobDescriptionData,
    ) -> AICoverLetter:

        payload = {
            "resume": resume.model_dump(),
            "job": job.model_dump(),
        }

        data = await self._generate_json(
            prompt_name="cover_letter",
            payload=payload,
            title="RAW COVER LETTER",
        )

        return AICoverLetter(
            **data,
        )
    
    async def generate_interview_questions(
        self,
        resume: ResumeData,
        job: JobDescriptionData,
    ) -> AIInterviewQuestions:

        payload = {
            "resume": resume.model_dump(),
            "job": job.model_dump(),
        }

        data = await self._generate_json(
            prompt_name="interview_questions",
            payload=payload,
            title="RAW INTERVIEW QUESTIONS",
        )

        return AIInterviewQuestions(
            **data,
        )
    
    async def generate_learning_roadmap(
        self,
        resume: ResumeData,
        job: JobDescriptionData,
        report: ATSResult,
    ) -> AILearningRoadmap:

        payload = {
            "resume": resume.model_dump(),
            "job": job.model_dump(),
            "ats_report": report.model_dump(),
        }

        data = await self._generate_json(
            prompt_name="learning_roadmap",
            payload=payload,
            title="RAW LEARNING ROADMAP",
        )

        return AILearningRoadmap(
            **data,
        )