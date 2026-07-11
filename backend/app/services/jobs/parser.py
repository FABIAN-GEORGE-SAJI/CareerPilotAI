import re

from app.schemas.job_data import JobDescriptionData


class JobParser:

    @staticmethod
    def parse(text: str) -> JobDescriptionData:

        return JobDescriptionData(
            title=JobParser.extract_title(text),
            company=JobParser.extract_company(text),
            summary=text[:500],
            skills=JobParser.extract_skills(text),
        )

    @staticmethod
    def extract_title(text: str) -> str:

        lines = [line.strip() for line in text.splitlines() if line.strip()]

        for i, line in enumerate(lines):

            lower = line.lower()

            if lower.startswith("job title"):

                if i + 1 < len(lines):
                    return lines[i + 1]

        ignore = {
            "job description",
            "sample job description",
            "overview",
            "responsibilities",
            "qualifications",
            "requirements",
            "about us",
        }

        for line in lines[:15]:

            if line.lower() in ignore:
                continue

            if 2 <= len(line.split()) <= 8:
                return line

        return ""

    @staticmethod
    def extract_company(text: str) -> str:

        # Look for "Company XYZ"
        match = re.search(
            r"\bCompany\s+([A-Z][A-Za-z0-9&., ]+?)(?:\s+is\b|\.|,|\n)",
            text
        )

        if match:
            return match.group(1).strip()

        return ""
    
    @staticmethod
    def extract_skills(text: str) -> list[str]:

        skills_database = [
            "Python",
            "Java",
            "C",
            "C++",
            "JavaScript",
            "TypeScript",
            "React",
            "Next.js",
            "FastAPI",
            "Django",
            "Flask",
            "SQL",
            "MySQL",
            "PostgreSQL",
            "MongoDB",
            "Git",
            "Docker",
            "Kubernetes",
            "Linux",
            "AWS",
            "Azure",
            "TensorFlow",
            "PyTorch",
            "Machine Learning",
            "Deep Learning",
            "NLP",
            "Excel",
            "Microsoft Word",
            "Communication",
            "Leadership",
            "Recruitment",
            "Human Resources",
            "HRIS",
            "Payroll",
        ]

        lower_text = text.lower()

        found_skills = []

        for skill in skills_database:
            pattern = r"\b" + re.escape(skill.lower()) + r"\b"

            if re.search(pattern, lower_text):
                found_skills.append(skill)

        return sorted(set(found_skills))