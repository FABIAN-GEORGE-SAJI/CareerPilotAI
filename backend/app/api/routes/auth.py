from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.dependencies import get_session
from app.schemas.user import AuthResponse, UserLogin, UserRegister
from app.services.auth.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/register",
    response_model=AuthResponse,
    summary="Register a new user",
    description="Creates a new user account and returns an access token, identical in shape to /auth/login. Fails with 400 if the email is already registered.",
)
def register(
    request: UserRegister,
    session: Session = Depends(get_session),
) -> AuthResponse:
    # ConflictError (duplicate email) is translated to a 400 response by the
    # global exception handler registered in main.py.
    auth_service = AuthService(session)
    return auth_service.register(request)


@router.post(
    "/login",
    response_model=AuthResponse,
    summary="Log in",
    description="Authenticates an existing user and returns an access token. Fails with 401 if the email/password combination is invalid.",
)
def login(
    request: UserLogin,
    session: Session = Depends(get_session),
) -> AuthResponse:
    # InvalidCredentialsError is translated to a 401 response by the global
    # exception handler registered in main.py.
    auth_service = AuthService(session)
    return auth_service.login(request)
