import json
from json import JSONDecodeError
from app.core.logging import logger

class JSONParser:
    """
    Safely extracts and parses JSON returned by LLMs.
    """

    @staticmethod
    def parse(text: str) -> dict:

        if not text:
            raise ValueError("Empty response from AI.")

        text = text.strip()

        # Locate the JSON object
        start = text.find("{")
        end = text.rfind("}")

        if start == -1 or end == -1:
            raise ValueError(
                "No JSON object found in AI response."
            )

        json_text = text[start:end + 1]

        try:
            return json.loads(json_text)

        except JSONDecodeError as e:

            logger.exception(
                "Failed to parse Gemini JSON response."
            )

            logger.error(
                "Raw AI response:\n%s",
                json_text,
            )

            raise ValueError(
                f"Invalid JSON returned by AI: {e}"
            ) from e