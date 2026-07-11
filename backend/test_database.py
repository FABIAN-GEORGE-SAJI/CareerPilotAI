from app.database.session import SessionLocal
from app.repositories.resume_repository import ResumeRepository


def main():

    session = SessionLocal()

    try:
        repository = ResumeRepository(session)

        resume = repository.save(
            filename="test_resume.pdf",
            parsed_data={
                "basic_info": {
                    "name": "John Doe",
                    "email": "john@example.com",
                    "phone": "1234567890",
                },
                "skills": [
                    "Python",
                    "FastAPI",
                    "SQLAlchemy",
                ],
            },
        )

        print("=" * 60)
        print("Resume Saved Successfully")
        print("=" * 60)
        print(f"ID: {resume.id}")
        print(f"Filename: {resume.filename}")
        print(f"Data: {resume.parsed_data}")

    finally:
        session.close()


if __name__ == "__main__":
    main()