from app.schemas.job_data import JobDescriptionData
from app.schemas.resume_data import ResumeData
from app.repositories.job_repository import JobRepository
from app.repositories.resume_repository import ResumeRepository
from app.services.matching.ats_scorer import ATSScorer
from app.database.session import SessionLocal

class MatchingService:

    def __init__(self):

        self.session = SessionLocal()

        self.resume_repository = ResumeRepository(
            self.session,
        )

        self.job_repository = JobRepository(
            self.session,
        )

        self.ats_scorer = ATSScorer()

    async def match(
        self,
        resume_id: int,
        job_id: int,
    ):
        resume_model = self.resume_repository.get_by_id(
            resume_id,
        )

        job_model = self.job_repository.get_by_id(
            job_id,
        )

        if resume_model is None:
            raise ValueError("Resume not found.")
        
        if job_model is None:
            raise ValueError("Job description not found.")
        
        resume = ResumeData(
            **resume_model.parsed_data,
        )

        resume = ResumeData(
            **resume_model.parsed_data,
        )

        job = JobDescriptionData(
            **job_model.parsed_data,
        )

        print("=" * 60)
        print("RESUME EDUCATION")
        print(resume.education)

        print("=" * 60)
        print("JOB QUALIFICATIONS")
        print(job.qualifications)

        print("=" * 60)
        print("RESUME SKILLS")
        print(resume.skills)

        print("=" * 60)
        print("JOB SKILLS")
        print(job.skills)
        print("=" * 60)

        report = await self.ats_scorer.score(
            resume,
            job,
        )

        return report