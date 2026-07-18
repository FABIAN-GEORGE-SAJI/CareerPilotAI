from sqlalchemy.orm import Session

from app.models.user import UserModel
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository[UserModel]):

    def __init__(self, session: Session):
        super().__init__(session)

    def get_by_email(self, email: str) -> UserModel | None:
        return self.session.query(UserModel).filter(UserModel.email == email).first()

    def get_by_username(self, username: str) -> UserModel | None:
        return self.session.query(UserModel).filter(UserModel.username == username).first()

    def create_user(
        self,
        email: str,
        name: str,
        password_hash: str,
    ) -> UserModel:
        user = UserModel(email=email, username=name, hashed_password=password_hash)
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user
    
    def get_by_id(self, user_id: int) -> UserModel | None:
        return (
            self.session.query(UserModel)
            .filter(UserModel.id == user_id)
            .first()
        )
