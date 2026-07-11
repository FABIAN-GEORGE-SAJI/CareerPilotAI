import fitz  # PyMuPDF
from pathlib import Path


class PDFParser:

    @staticmethod
    def extract_text(pdf_path: Path) -> str:
        """
        Extract all text from a PDF.
        """

        document = fitz.open(pdf_path)

        text = ""

        for page in document:
            text += page.get_text()

        document.close()

        return text.strip()