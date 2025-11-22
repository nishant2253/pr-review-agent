from fastapi import APIRouter, HTTPException

from app.models.review_request import ReviewPRRequest, ReviewDiffRequest
from app.models.review_response import ReviewResponse
from app.services.review_orchestrator import run_review_for_pr, run_review_for_diff

router = APIRouter()


@router.post("/diff", response_model=ReviewResponse)
async def review_diff(request: ReviewDiffRequest):
    return await run_review_for_diff(request)


@router.post("/pr", response_model=ReviewResponse)
async def review_pr(request: ReviewPRRequest):
    try:
        return await run_review_for_pr(
            owner=request.owner,
            repo=request.repo,
            pr_number=request.pr_number
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
