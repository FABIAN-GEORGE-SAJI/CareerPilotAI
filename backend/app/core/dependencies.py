from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError
from sqlalchemy.orm import Session

from app.core.security import decode_access_token
from app.database.dependencies import get_session
from app.models.user import UserModel

security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: Session = Depends(get_session),
) -> UserModel:
    """Resolves the authenticated user from a bearer JWT.

    NOTE: this dependency is not currently attached to any route. Every
    frontend request already carries the Authorization header (see
    frontend/api.py::CareerPilotAPI.headers), but no endpoint requires or
    verifies it yet - the API is effectively unauthenticated today.
    Wiring `Depends(get_current_user)` into the resume/jobs/match/ai/
    career-agent routes would enforce it; that's a deliberate product/
    security decision left to the project owner rather than something this
    refactor changes silently, since it would start rejecting any request
    that doesn't carry a valid token.

    The previous version of this function had a bug that would have made it
    fail at import/runtime regardless: `credentials`/`session` were declared
    as `Depends(...)` used as the *type annotation* itself
    (e.g. `credentials: Depends(security)`), instead of `Depends(...)` used
    as the parameter default (`credentials: HTTPAuthorizationCredentials =
    Depends(security)`), which is what FastAPI actually requires to resolve
    the dependency.
    """
    try:
        payload = decode_access_token(credentials.credentials)
        user_id = int(payload["sub"])
        user = session.get(UserModel, user_id)

        if not user:
            raise HTTPException(
                status_code=401,
                detail="User not found.",
            )

        if not user.is_active:
            raise HTTPException(
                status_code=403,
                detail="User account is disabled.",
            )

        return user
    except (JWTError, KeyError, ValueError):
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication token.",
        )
