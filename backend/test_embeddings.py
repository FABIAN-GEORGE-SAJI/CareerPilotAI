from app.services.embeddings.embedding_service import EmbeddingService

service = EmbeddingService()

print(
    service.similarity(
        "Python",
        "Python"
    )
)

print(
    service.similarity(
        "MySQL",
        "SQL"
    )
)

print(
    service.similarity(
        "Pandas",
        "Data Analysis"
    )
)

print(
    service.similarity(
        "Docker",
        "Kubernetes"
    )
)