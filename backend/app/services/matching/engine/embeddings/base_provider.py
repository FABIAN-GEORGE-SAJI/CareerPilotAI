from abc import ABC, abstractmethod

from app.schemas.embedding_result import EmbeddingResult


class BaseEmbeddingProvider(ABC):

    @abstractmethod
    async def embed(
        self,
        texts: list[str],
    ) -> EmbeddingResult:
        pass