from typing import List, Dict
from pydantic import BaseModel


class AgentComment(BaseModel):
    agent: str
    comment: str
    file: str = ""
    line: int | None = None


class ReviewResponse(BaseModel):
    message: str
    comments: List[AgentComment]
    summary: str | None = None
