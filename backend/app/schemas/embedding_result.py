from pydantic import BaseModel, Field

import numpy as np


class EmbeddingResult(BaseModel):
    """
    Result returned by an embedding provider.
    """
    texts: list[str] = Field(default_factory=list)

    vectors: list[np.ndarray] = Field(default_factory=list)

    model: str = ""

    dimension: int = 0

    normalized: bool = False

    class Config:
        arbitrary_types_allowed = True