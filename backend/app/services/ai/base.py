from abc import ABC, abstractmethod

from app.schemas.ats_result import ATSResult
from app.schemas.job_data import JobDescriptionData
from app.schemas.resume_data import ResumeData


class AIService(ABC):

    @abstractmethod
    async def parse_resume(self, text: str) -> ResumeData:
        pass

    @abstractmethod
    async def parse_job(self, text: str) -> JobDescriptionData:
        pass

    @abstractmethod
    async def generate_feedback(
        self,
        report: ATSResult,
    ) -> str:
        pass

    @abstractmethod
    async def rewrite_resume(
        self,
        resume: ResumeData,
        job: JobDescriptionData,
    ) -> str:
        pass

    @abstractmethod
    async def generate_cover_letter(
        self,
        resume: ResumeData,
        job: JobDescriptionData,
    ) -> str:
        pass