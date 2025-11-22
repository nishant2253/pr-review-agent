from pydantic import BaseModel

class ReviewPRRequest(BaseModel):
    owner: str
    repo: str
    pr_number: int

class ReviewDiffRequest(BaseModel):
    diff: str
