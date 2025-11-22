# app/services/review_orchestrator.py

import asyncio
from typing import List, Dict, Any

from app.models.review_response import ReviewResponse
from app.services.diff_parser import parse_diff
from app.services.github_service import fetch_pr_diff

# Agent imports
from app.agents.logic_agent import run_logic_agent
from app.agents.readability_agent import run_readability_agent
from app.agents.performance_agent import run_performance_agent
from app.agents.security_agent import run_security_agent
from app.agents.aggregator_agent import aggregate_comments

from app.core.logger import logger


def _build_diff_text(parsed_diff: List[Dict[str, Any]]) -> str:
    """Convert parsed diff into a single plain text chunk."""
    diff_text = ""
    for file in parsed_diff:
        diff_text += f"\nFile: {file.get('filename')}\n"
        diff_text += file.get("patch", "") + "\n"
    return diff_text


async def _run_multi_agent_review(parsed_diff: List[Dict[str, Any]]) -> ReviewResponse:
    diff_text = _build_diff_text(parsed_diff)

    logger.info("🚀 Running multi-agent review...")

    # Create async tasks for each agent
    logic_task = run_logic_agent(diff_text)
    read_task = run_readability_agent(diff_text)
    perf_task = run_performance_agent(diff_text)
    sec_task = run_security_agent(diff_text)

    # Run all agents concurrently
    (
        logic_comments,
        readability_comments,
        performance_comments,
        security_comments,
    ) = await asyncio.gather(
        logic_task,
        read_task,
        perf_task,
        sec_task,
    )

    all_comments_raw = (
        logic_comments
        + readability_comments
        + performance_comments
        + security_comments
    )

    logger.info(f"Collected {len(all_comments_raw)} raw comment(s) from all agents.")

    # Use aggregator to create final ReviewResponse
    return aggregate_comments(all_comments_raw)


async def run_review_for_diff(request):
    """Main entrypoint for /review/diff"""
    diff_text = request.diff
    parsed = parse_diff(diff_text)
    return await _run_multi_agent_review(parsed)


async def run_review_for_pr(owner: str, repo: str, pr_number: int) -> ReviewResponse:
    """
    Phase 5: Full GitHub PR integration.

    - Fetches diff from GitHub
    - Parses diff
    - Runs the same multi-agent pipeline as /review/diff
    """
    # 1) Fetch diff from GitHub
    diff_text = await fetch_pr_diff(owner, repo, pr_number)

    # 2) Parse unified diff into structured chunks
    parsed = parse_diff(diff_text)

    # 3) Run agents + aggregation
    return await _run_multi_agent_review(parsed)
