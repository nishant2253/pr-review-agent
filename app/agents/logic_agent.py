from typing import List, Dict, Any
from app.agents.base_agent import call_review_agent


async def run_logic_agent(diff_text: str) -> List[Dict[str, Any]]:
    """
    Analyze diff for logical correctness, bugs, and edge cases.
    """
    guidelines = """
Focus on:
- Incorrect conditions (== vs !=, > vs >=, etc.)
- Off-by-one errors in loops or ranges
- Incorrect or missing edge case handling (nulls, empties, boundaries)
- Wrong return values or early returns
- Misused boolean logic (AND/OR)
Ignore style and formatting here; only logic.
"""
    return await call_review_agent(
        role_description="LOGIC and bug detection",
        guidelines=guidelines,
        diff_text=diff_text,
    )
