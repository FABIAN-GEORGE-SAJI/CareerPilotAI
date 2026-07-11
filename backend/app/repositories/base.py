from typing import Generic, TypeVar

from sqlalchemy.orm import Session

ModelType = TypeVar("ModelType")


class BaseRepository(Generic[ModelType]):

    def __init__(self, session: Session):
        self.session = session

    def add(self, obj: ModelType) -> ModelType:

        self.session.add(obj)
        self.session.commit()
        self.session.refresh(obj)

        return obj

    def get_by_id(self, model: type[ModelType], obj_id: int):

        return self.session.get(model, obj_id)

    def delete(self, obj: ModelType):

        self.session.delete(obj)
        self.session.commit()

    def update(self):

        self.session.commit()