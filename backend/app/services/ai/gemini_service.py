from google import genai
from app.schemas.ai_job import AIJob
from app.services.mapping.job_mapper import JobMapper
from app.core.config import settings

from app.schemas.ai_resume import AIResume
from app.schemas.ats_result import ATSResult
from app.schemas.job_data import JobDescriptionData
from app.schemas.resume_data import ResumeData

from app.services.ai.base import AIService
from app.services.mapping.resume_mapper import ResumeMapper

from app.utils.json_parser import JSONParser
from app.utils.prompt_loader import PromptLoader
from app.schemas.ai_experience_score import AIExperienceScore


class GeminiService(AIService):

    def __init__(self):

        self.client = genai.Client(
            api_key=settings.GEMINI_API_KEY
        )

        self.model = settings.GEMINI_MODEL

    async def generate_text(self, prompt: str) -> str:

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
        )

        return response.text.strip()

    async def parse_resume(self, text: str) -> ResumeData:

        prompt = PromptLoader.load("resume_parser")

        full_prompt = "\n\n".join([
            prompt,
            "Resume:",
            text,
        ])

        response = await self.generate_text(full_prompt)

        # Temporary debugging (remove later)
        print("\n" + "=" * 80)
        print("RAW GEMINI RESPONSE")
        print("=" * 80)
        print(response)
        print("=" * 80 + "\n")

        data = JSONParser.parse(response)

        ai_resume = AIResume(**data)

        return ResumeMapper.to_resume_data(ai_resume)

    async def parse_job(self, text: str) -> JobDescriptionData:

        prompt = PromptLoader.load("job_parser")

        full_prompt = "\n\n".join([
            prompt,
            "Job Description:",
            text,
        ])

        response = await self.generate_text(full_prompt)

        print("\n" + "=" * 80)
        print("RAW GEMINI JOB RESPONSE")
        print("=" * 80)
        print(response)
        print("=" * 80 + "\n")

        data = JSONParser.parse(response)

        ai_job = AIJob(**data)

        return JobMapper.to_job_data(ai_job)
    async def score_experience(
        self,
        resume: ResumeData,
        job: JobDescriptionData,
    ) -> AIExperienceScore:

        prompt = PromptLoader.load("experience_score")

        full_prompt = "\n\n".join([
            prompt,
            "Resume Experience:",
            str(resume.experience),
            "",
            "Job Description:",
            str(job),
        ])

        response = await self.generate_text(full_prompt)

        print("\n" + "=" * 80)
        print("RAW EXPERIENCE SCORE")
        print("=" * 80)
        print(response)
        print("=" * 80 + "\n")

        data = JSONParser.parse(response)

        return AIExperienceScore(**data)

    async def generate_feedback(
        self,
        report: ATSResult,
    ) -> str:
        raise NotImplementedError

    async def rewrite_resume(
        self,
        resume: ResumeData,
        job: JobDescriptionData,
    ) -> str:
        raise NotImplementedError

    async def generate_cover_letter(
        self,
        resume: ResumeData,
        job: JobDescriptionData,
    ) -> str:
        raise NotImplementedError