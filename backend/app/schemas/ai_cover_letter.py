from pydantic import BaseModel


class AICoverLetter(BaseModel):

    subject: str = ""

    greeting: str = ""

    body: str = ""

    closing: str = ""