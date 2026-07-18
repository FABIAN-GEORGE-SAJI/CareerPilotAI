"""Shared request validation helpers.

Kept deliberately small: this centralizes the upload checks that used to be
duplicated (and incomplete) across app/api/routes/resume.py and
app/api/routes/jobs.py.
"""

from pathlib import Path

from fastapi import HTTPException, UploadFile

from app.core.config import settings

# Business rule: both /resume/upload and /jobs/upload only ever accepted PDF,
# regardless of the broader ALLOWED_EXTENSIONS list in settings (which also
# covers .docx for future use). Keeping this scoped to PDF preserves the
# existing API contract - it does not widen or narrow what today's frontend
# can already do.
_ACCEPTED_UPLOAD_EXTENSIONS = {".pdf"}


async def validate_upload_file(file: UploadFile) -> bytes:
    """Validates an uploaded document before it's parsed.

    Checks (in order): a filename is present, the extension is supported,
    the file is not empty, and it does not exceed the configured size limit.
    Raises HTTPException(400) with a descriptive message on failure.

    Returns the file's raw bytes so callers that already need them (e.g. to
    extract text) don't have to read the upload a second time. The file's
    read position is reset afterwards so downstream code can read it again
    if it prefers to work with the UploadFile directly.
    """

    if not file.filename:
        raise HTTPException(status_code=400, detail="No file was uploaded.")

    extension = Path(file.filename).suffix.lower()
    if extension not in _ACCEPTED_UPLOAD_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    content = await file.read()
    await file.seek(0)

    if not content:
        raise HTTPException(status_code=400, detail="The uploaded file is empty.")

    max_bytes = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024
    if len(content) > max_bytes:
        raise HTTPException(
            status_code=400,
            detail=f"File exceeds the {settings.MAX_UPLOAD_SIZE_MB}MB upload limit.",
        )

    return content
