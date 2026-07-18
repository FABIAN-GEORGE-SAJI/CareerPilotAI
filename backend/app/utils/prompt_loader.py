from functools import lru_cache
from pathlib import Path

PROMPTS_DIR = Path(__file__).resolve().parents[1] / "prompts"


class PromptLoader:

    @staticmethod
    @lru_cache(maxsize=None)
    def load(prompt_name: str) -> str:

        prompt_file = PROMPTS_DIR / f"{prompt_name}.txt"

        if not prompt_file.exists():
            raise FileNotFoundError(
                f"Prompt '{prompt_name}' not found."
            )

        return prompt_file.read_text(
            encoding="utf-8"
        )