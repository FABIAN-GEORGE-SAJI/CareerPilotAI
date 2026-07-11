from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim


class EmbeddingService:
    """
    Generates sentence embeddings and computes similarity.
    """

    def __init__(self):
        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

    def similarity(
        self,
        text1: str,
        text2: str,
    ) -> float:

        embedding1 = self.model.encode(
            text1,
            convert_to_tensor=True,
        )

        embedding2 = self.model.encode(
            text2,
            convert_to_tensor=True,
        )

        return float(
            cos_sim(
                embedding1,
                embedding2,
            )
        )