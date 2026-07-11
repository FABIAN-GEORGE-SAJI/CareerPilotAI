class ExactMatcher:
    """
    Performs exact skill matching.
    """

    @staticmethod
    def match(
        resume_skills: list[str],
        job_skills: list[str],
    ) -> set[str]:

        resume = {
            skill.strip().lower()
            for skill in resume_skills
        }

        job = {
            skill.strip().lower()
            for skill in job_skills
        }

        return resume & job