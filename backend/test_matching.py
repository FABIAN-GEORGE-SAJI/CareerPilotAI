from app.schemas.resume_data import ResumeData, BasicInfo
from app.schemas.job_data import JobDescriptionData
from app.services.matching.matcher import MatchingService


resume = ResumeData(
    basic_info=BasicInfo(
        name="Fabian",
        email="fabian@example.com",
        phone="9999999999",
    ),
    skills=[
        "Python",
        "Docker",
        "Git",
        "SQL",
    ]
)

job = JobDescriptionData(
    skills=[
        "Python",
        "Docker",
        "AWS",
        "Git",
    ]
)

report = MatchingService.compare(
    resume,
    job
)

print(report.model_dump())