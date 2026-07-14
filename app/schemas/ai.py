from pydantic import BaseModel


class MusicPrompt(BaseModel):
    prompt: str
    duration: int = 10