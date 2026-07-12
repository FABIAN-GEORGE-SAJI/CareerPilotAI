from pprint import pprint

from app.services.matching.engine.knowledge.knowledge_service import (
    KnowledgeService,
)

service = KnowledgeService()

print()

pprint(
    service.search(
        "Amazon Web Services"
    )
)

print()

pprint(
    service.search(
        "AWS"
    )
)