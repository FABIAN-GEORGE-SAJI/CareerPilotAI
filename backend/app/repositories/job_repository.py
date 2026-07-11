from app.models.job import JobModel
from app.repositories.base import BaseRepository


class JobRepository(BaseRepository[JobModel]):

    def save(
        self,
        filename: str,
        parsed_data: dict,
    ) -> JobModel:

        job = JobModel(
            filename=filename,
            parsed_data=parsed_data,
        )

        return self.add(job)
    
    def get_by_id(
        self,
        job_id: int,
    ) -> JobModel:

        return super().get_by_id(
            JobModel,
            job_id,
        )