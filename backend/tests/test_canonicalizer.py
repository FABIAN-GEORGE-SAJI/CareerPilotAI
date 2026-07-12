from app.services.matching.engine.knowledge.canonicalizer import (
    Canonicalizer,
)

c = Canonicalizer()

print()

print(
    c.canonicalize(
        [
            "AWS",
            "Amazon Web Services",
            "Amazon AWS",
            "Python",
            "Python3",
        ]
    )
)