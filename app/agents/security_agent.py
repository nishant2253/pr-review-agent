from typing import List, Dict, Any
from app.agents.base_agent import call_review_agent


async def run_security_agent(diff_text: str) -> List[Dict[str, Any]]:
    """
    Analyze diff for security vulnerabilities.
    """
    guidelines = """
Focus on:
- Unsanitized user input reaching SQL, shell commands, eval, etc.
- Hard-coded secrets, API keys, passwords, tokens
- Insecure use of cryptography or insecure randomness
- Missing authorization checks on sensitive operations
- Path traversal or unsafe file handling
Use "SECURITY" as category.
Only flag meaningful risks, not generic style comments.
"""
    return await call_review_agent(
        role_description="SECURITY and vulnerability detection",
        guidelines=guidelines,
        diff_text=diff_text,
    )
