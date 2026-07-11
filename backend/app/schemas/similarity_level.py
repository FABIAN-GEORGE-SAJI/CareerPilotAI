from enum import Enum


class SimilarityLevel(str, Enum):

    EXACT = "Exact"

    EQUIVALENT = "Equivalent"

    VERY_STRONG = "Very Strong"

    STRONG = "Strong"

    RELATED = "Related"

    WEAK = "Weak"

    NONE = "None"