from typing import List, Dict, Any
from app.agents.base_agent import call_review_agent


async def run_readability_agent(diff_text: str) -> List[Dict[str, Any]]:
    """
    Analyze diff for readability and maintainability issues.
    """
    guidelines = """
Focus on:
- Unclear or misleading names for variables, functions, classes
- Overly long or deeply nested functions
- Missing comments where logic is non-obvious
- Inconsistent style that makes code harder to read
Do NOT comment on logic unless it clearly hurts readability.
Use "READABILITY" as category.
"""
    return await call_review_agent(
        role_description="READABILITY and maintainability",
        guidelines=guidelines,
        diff_text=diff_text,
    )
