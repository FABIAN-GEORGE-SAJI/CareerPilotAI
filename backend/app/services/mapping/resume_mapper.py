from app.schemas.ai_resume import AIResume
from app.schemas.entities import (
    Education,
    Experience,
    Project,
    Certification,
)
from app.schemas.resume_data import (
    ResumeData,
    BasicInfo,
)


class ResumeMapper:

    @staticmethod
    def to_resume_data(ai_resume: AIResume) -> ResumeData:

        return ResumeData(

            basic_info=BasicInfo(
                name=ai_resume.basic_info.name,
                email=ai_resume.basic_info.email,
                phone=ai_resume.basic_info.phone,
            ),

            skills=ai_resume.skills,

            education=[
                Education(
                    degree=e.degree,
                    institution=e.institution,
                    graduation_year=e.year,
                )
                for e in ai_resume.education
            ],

            experience=[
                Experience(
                    company=e.company,
                    position=e.title,
                    start_date="",
                    end_date=e.duration,
                    description=e.description,
                )
                for e in ai_resume.experience
            ],

            projects=[
                Project(
                    title=p.name,
                    technologies=p.technologies,
                    description=p.description,
                )
                for p in ai_resume.projects
            ],

            certifications=[
                Certification(
                    name=c.name,
                    issuer=c.issuer,
                )
                for c in ai_resume.certifications
            ],

            languages=ai_resume.languages,

            summary=ai_resume.summary,
        )