# app/services/github_service.py

from typing import Optional

import httpx

from app.core.settings import settings
from app.core.logger import logger

GITHUB_API_BASE = "https://api.github.com"


async def fetch_pr_diff(owner: str, repo: str, pr_number: int) -> str:
    """
    Fetch the unified diff for a GitHub PR using the GitHub REST API.

    - Uses optional GITHUB_TOKEN from env for higher rate limits.
    - Returns the raw diff text.
    - Raises an Exception if PR is not found or request fails.
    """
    headers = {
        "Accept": "application/vnd.github.v3.diff",
        "User-Agent": "pr-review-agent",
    }

    if settings.GITHUB_TOKEN:
        headers["Authorization"] = f"token {settings.GITHUB_TOKEN}"

    url = f"{GITHUB_API_BASE}/repos/{owner}/{repo}/pulls/{pr_number}"

    logger.info(f" Fetching PR diff for {owner}/{repo}#{pr_number}")

    async with httpx.AsyncClient(timeout=20) as client:
        resp = await client.get(url, headers=headers)

    if resp.status_code == 404:
        logger.error("❌ PR not found")
        raise Exception("PR not found. Check owner/repo/pr_number.")
    if resp.status_code >= 400:
        logger.error(f"❌ GitHub API error {resp.status_code}: {resp.text}")
        raise Exception(f"GitHub API error: {resp.status_code}")

    logger.info("Successfully fetched PR diff from GitHub")
    return resp.text
