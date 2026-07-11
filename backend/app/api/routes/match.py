from fastapi import APIRouter

from app.schemas.match import MatchRequest, MatchResponse
from app.services.matching.matching_service import MatchingService

router = APIRouter(
    prefix="/match",
    tags=["Matching"]
)


@router.post(
    "",
    response_model=MatchResponse
)
async def match_resume(request: MatchRequest):

    matching_service = MatchingService()
    report = await matching_service.match(
        request.resume_id,
        request.job_id,
    )

    return MatchResponse(
        report=report
    )