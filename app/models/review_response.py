from pydantic import BaseModel
from typing import List
from app.models.review_comment import ReviewComment

class ReviewResponse(BaseModel):
    summary: str
    comments: List[ReviewComment]
