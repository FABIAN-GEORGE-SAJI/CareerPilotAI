from sentence_transformers import SentenceTransformer

from app.schemas.embedding_result import EmbeddingResult
from app.services.matching.engine.embeddings.base_provider import (
    BaseEmbeddingProvider,
)


class SentenceTransformerProvider(BaseEmbeddingProvider):
    """
    Generates embeddings using Sentence Transformers.
    """

    def __init__(self):

        self.model = SentenceTransformer(
            "BAAI/bge-small-en-v1.5"
        )

    async def embed(
        self,
        texts: list[str],
    ) -> EmbeddingResult:

        vectors = self.model.encode(
            texts,
            normalize_embeddings=True,
            convert_to_numpy=True,
        )

        return EmbeddingResult(

            texts=texts,

            vectors=list(vectors),

            model="BAAI/bge-small-en-v1.5",

            dimension=self.model.get_embedding_dimension(),

            normalized=True,
        )