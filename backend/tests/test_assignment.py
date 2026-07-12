from app.schemas.semantic_match_result import (
    SemanticSkillMatch,
)

from app.services.matching.engine.assignment.greedy_assignment import (
    GreedyAssignment,
)

matches = [

    SemanticSkillMatch(
        resume_skill="Python",
        job_skill="Python",
        similarity=1.0,
    ),

    SemanticSkillMatch(
        resume_skill="Python",
        job_skill="Machine Learning",
        similarity=0.82,
    ),

    SemanticSkillMatch(
        resume_skill="SQL",
        job_skill="MySQL",
        similarity=0.84,
    ),

]

assigned = GreedyAssignment.assign(matches)

print()

for m in assigned:

    print(
        m.resume_skill,
        "->",
        m.job_skill,
        m.similarity,
    )