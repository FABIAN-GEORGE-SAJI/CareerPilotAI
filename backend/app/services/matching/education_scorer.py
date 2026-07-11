from app.schemas.job_data import JobDescriptionData
from app.schemas.resume_data import ResumeData
from app.services.matching.base_scorer import BaseScorer

class EducationScorer(BaseScorer):
    """
    Scores the education section of a resume.
    """

    async def score(
        self,
        resume: ResumeData,
        job: JobDescriptionData,
    ) -> float:

        # If the job doesn't specify education,
        # don't penalize the candidate.
        if not job.qualifications:
            return 100.0

        # If the candidate has any education,
        # award full marks for now.
        if resume.education:
            return 100.0

        return 0.0