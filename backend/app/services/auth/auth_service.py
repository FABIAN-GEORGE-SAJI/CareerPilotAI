from sqlalchemy.orm import Session

from app.core.exceptions import ConflictError, InvalidCredentialsError
from app.core.security import create_access_token, hash_password, verify_password
from app.repositories.user_repository import UserRepository
from app.schemas.user import AuthResponse, Token, UserLogin, UserRegister, UserResponse


class AuthService:

    def __init__(self, session: Session):
        self.repository = UserRepository(session)

    def register(self, request: UserRegister) -> AuthResponse:
        existing = self.repository.get_by_email(request.email)

        if existing:
            raise ConflictError("Email already registered.")

        user = self.repository.create_user(
            email=request.email,
            name=request.name,
            password_hash=hash_password(request.password),
        )

        token = create_access_token(user.id)

        return AuthResponse(
            user=UserResponse(
                id=user.id,
                name=user.username,
                email=user.email,
                is_active=user.is_active,
            ),
            token=Token(access_token=token),
        )

    def login(self, request: UserLogin) -> AuthResponse:
        user = self.repository.get_by_email(request.email)

        if not user or not verify_password(request.password, user.hashed_password):
            raise InvalidCredentialsError("Invalid email or password.")

        token = create_access_token(user.id)

        return AuthResponse(
            user=UserResponse(
                id=user.id,
                name=user.username,
                email=user.email,
                is_active=user.is_active,
            ),
            token=Token(access_token=token),
        )
