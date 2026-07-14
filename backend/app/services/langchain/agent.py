from langchain.agents import create_agent

from app.services.langchain.model import llm
from app.services.langchain.prompts import (
    CAREER_AGENT_PROMPT,
)
from app.services.langchain.tools import TOOLS


career_agent = create_agent(
    model=llm,
    tools=TOOLS,
    system_prompt=CAREER_AGENT_PROMPT.messages[0].prompt.template,
)