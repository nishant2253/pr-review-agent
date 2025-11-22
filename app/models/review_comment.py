from pydantic import BaseModel
from typing import Optional

class ReviewComment(BaseModel):
    file: str
    line: Optional[int] = None
    severity: str
    category: str
    comment: str
    suggestion: Optional[str] = None
