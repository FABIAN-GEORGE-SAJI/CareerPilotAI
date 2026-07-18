from pypdf import PdfReader
from fastapi import UploadFile

async def extract_text_from_pdf(file: UploadFile) -> str:
    """Extracts raw text from an uploaded PDF file."""
    text = ""
    reader = PdfReader(file.file)
    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + "\n"
    
    # Reset file pointer in case it needs to be read again
    await file.seek(0)
    return text.strip()