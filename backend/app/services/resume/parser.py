
import re
from app.schemas.resume_data import ResumeData, BasicInfo

SECTION_HEADINGS = {
    "SUMMARY",
    "EDUCATION",
    "EXPERIENCE",
    "WORK EXPERIENCE",
    "SKILLS",
    "PROJECTS",
    "CERTIFICATIONS",
    "ACHIEVEMENTS",
    "LANGUAGES",
}


class ResumeParser:

    @staticmethod
    def parse(text: str) -> dict:

        email = ResumeParser.extract_email(text)
        phone = ResumeParser.extract_phone(text)
        name = ResumeParser.extract_name(text)
        sections = ResumeParser.extract_sections(text)

        return ResumeData(

            basic_info=BasicInfo(
                name=name,
                email=email,
                phone=phone,
            ),

            sections=sections,
        )


    @staticmethod
    def extract_email(text: str) -> str:

        match = re.search(
            r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
            text
        )

        return match.group(0) if match else ""
    

    @staticmethod
    def extract_phone(text: str) -> str:

        match = re.search(
            r"(\+?\d[\d\s\-]{8,}\d)",
            text
        )

        return match.group(0) if match else ""
    

    @staticmethod
    def extract_name(text: str) -> str:

        lines = text.splitlines()

        for line in lines:

            line = line.strip()

            if len(line.split()) >= 2 and len(line) < 40:

                if "@" not in line:

                    return line

        return ""
    

    @staticmethod
    def extract_sections(text: str) -> dict[str, list[str]]:


        sections = {}
        current_section = "HEADER"
        sections[current_section] = []

        for line in text.splitlines():

            line = line.strip()

            if not line:
                continue

            upper = line.upper()

            normalized = upper.replace(":", "").strip()

            if any(h in normalized for h in SECTION_HEADINGS):
                current_section = normalized
                sections[current_section] = []
                continue

            sections[current_section].append(line)

        return sections