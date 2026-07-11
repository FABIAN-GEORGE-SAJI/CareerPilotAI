from app.schemas.job_data import JobDescriptionData
from app.schemas.resume_data import ResumeData
from app.services.matching.base_scorer import BaseScorer


class ProjectScorer(BaseScorer):
    """
    Scores resume projects against the job description.
    """

    async def score(
        self,
        resume: ResumeData,
        job: JobDescriptionData,
    ) -> float:

        if not resume.projects:
            return 0.0

        job_skills = {
            skill.strip().lower()
            for skill in job.skills
        }

        if not job_skills:
            return 100.0

        project_technologies = set()

        project_descriptions = []

        for project in resume.projects:

            project_technologies.update(
                tech.strip().lower()
                for tech in project.technologies
            )

            project_descriptions.extend(
                line.lower()
                for line in project.description
            )

        # ---------- Technology Score ----------

        matched_tech = (
            project_technologies &
            job_skills
        )

        tech_score = (
            len(matched_tech)
            /
            len(job_skills)
        ) * 100

        # ---------- Description Score ----------

        responsibility_matches = 0

        for responsibility in job.responsibilities:

            responsibility = responsibility.lower()

            if any(
                responsibility in description
                or description in responsibility
                for description in project_descriptions
            ):
                responsibility_matches += 1

        if job.responsibilities:

            description_score = (
                responsibility_matches
                /
                len(job.responsibilities)
            ) * 100

        else:

            description_score = 100

        # ---------- Final ----------

        final_score = (
            tech_score * 0.7
            +
            description_score * 0.3
        )

        return round(
            final_score,
            2,
        )