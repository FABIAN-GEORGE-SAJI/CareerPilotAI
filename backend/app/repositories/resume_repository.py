from app.models.resume import ResumeModel
from app.repositories.base import BaseRepository


class ResumeRepository(BaseRepository[ResumeModel]):

    def save(
        self,
        filename: str,
        parsed_data: dict,
    ) -> ResumeModel:

        resume = ResumeModel(
            filename=filename,
            parsed_data=parsed_data,
        )

        return self.add(resume)
    
    def get_by_id(
        self,
        resume_id: int,
    ) -> ResumeModel:

        return super().get_by_id(
            ResumeModel,
            resume_id,
        )