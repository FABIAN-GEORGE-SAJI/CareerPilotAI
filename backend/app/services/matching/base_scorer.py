from abc import ABC, abstractmethod

from app.schemas.job_data import JobDescriptionData
from app.schemas.resume_data import ResumeData


class BaseScorer(ABC):
    """
    Base class for all ATS scorers.
    """

    @abstractmethod
    async def score(
        self,
        resume: ResumeData,
        job: JobDescriptionData,
    ):
        """
        Score a resume against a job description.
        """
        pass