from app.schemas.ai_job import AIJob
from app.schemas.job_data import JobDescriptionData


class JobMapper:

    @staticmethod
    def to_job_data(ai_job: AIJob) -> JobDescriptionData:

        return JobDescriptionData(
            title=ai_job.title,
            company=ai_job.company,
            summary=ai_job.summary,
            skills=ai_job.skills,
            required_skills=ai_job.required_skills,
            preferred_skills=ai_job.preferred_skills,
            soft_skills=ai_job.soft_skills,
            responsibilities=ai_job.responsibilities,
            qualifications=ai_job.qualifications,
            location=ai_job.location,
            employment_type=ai_job.employment_type,
            experience=ai_job.experience,
            education=ai_job.education,
            keywords=ai_job.keywords,
        )