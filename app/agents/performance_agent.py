from typing import List, Dict, Any
from app.agents.base_agent import call_review_agent


async def run_performance_agent(diff_text: str) -> List[Dict[str, Any]]:
    """
    Analyze diff for performance problems.
    """
    guidelines = """
Focus on:
- Inefficient loops, especially nested loops over large collections
- Repeated calculations that could be cached or precomputed
- N+1 query patterns or repeated I/O
- Use of heavy operations in hot paths
Ignore micro-optimizations; only flag realistic performance risks.
Use "PERFORMANCE" as category.
"""
    return await call_review_agent(
        role_description="PERFORMANCE and efficiency",
        guidelines=guidelines,
        diff_text=diff_text,
    )
