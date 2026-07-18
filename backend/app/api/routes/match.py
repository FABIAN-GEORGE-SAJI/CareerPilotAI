from fastapi import APIRouter, Depends
from app.api.dependencies import get_current_user
from app.models.user import UserModel
from app.api.dependencies import get_matching_service
from app.schemas.match import MatchRequest
from app.services.matching.matching_service import MatchingService

router = APIRouter(
    tags=["ATS Matching"],
)


@router.post(
    "",
    summary="Generate an ATS match report",
    description=(
        "Scores a previously-uploaded resume against a previously-uploaded "
        "job description and returns the ATS match report (overall score, "
        "matched/missing skills, and supporting analysis)."
    ),
)
async def generate_match(
    request: MatchRequest,
    matching_service: MatchingService = Depends(get_matching_service),
    current_user: UserModel = Depends(get_current_user),
):
    # MatchingService owns resume/job lookup and ATS scoring - this route no
    # longer duplicates that logic. A NotFoundError from the service is
    # translated into a 404 response by the global exception handler
    # registered in main.py; any other failure falls through to the generic
    # 500 handler (and is logged there) rather than being swallowed here.
    report = await matching_service.match(request.resume_id, request.job_id)

    # Response shape kept identical to before - pages/3_ATS.py expects this.
    return {
        "message": "ATS Analysis complete.",
        "report": report.model_dump(),
    }
