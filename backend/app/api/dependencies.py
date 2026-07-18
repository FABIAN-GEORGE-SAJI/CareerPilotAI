from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError
from sqlalchemy.orm import Session

from app.core.security import decode_access_token
from app.database.dependencies import get_session
from app.repositories.user_repository import UserRepository

from app.services.ai.gemini_service import GeminiService
from app.services.matching.matching_service import MatchingService


def get_matching_service(session: Session = Depends(get_session)) -> MatchingService:
    """Provides a MatchingService bound to the current request's session.

    Using FastAPI's dependency injection here (rather than the service
    opening its own session) ensures the session is closed when the request
    ends - see app.database.dependencies.get_session.
    """
    return MatchingService(session)


def get_gemini_service() -> GeminiService:
    return GeminiService()
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError

security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: Session = Depends(get_session),
):
    try:
        payload = decode_access_token(credentials.credentials)
        user_id = int(payload["sub"])

        repository = UserRepository(session)
        user = repository.get_by_id(user_id)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is inactive",
            )

        return user

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

