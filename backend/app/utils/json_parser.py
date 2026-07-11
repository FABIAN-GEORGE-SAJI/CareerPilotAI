import json
from json import JSONDecodeError


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

            print("\n" + "=" * 80)
            print("FAILED TO PARSE JSON")
            print("=" * 80)
            print(json_text)
            print("=" * 80 + "\n")

            raise ValueError(
                f"Invalid JSON returned by AI: {e}"
            ) from e