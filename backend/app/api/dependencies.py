from app.services.ai.gemini_service import GeminiService
from app.services.matching.matching_service import MatchingService


def get_matching_service() -> MatchingService:
    return MatchingService()


def get_gemini_service() -> GeminiService:
    return GeminiService()