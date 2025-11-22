import json
import re
from typing import List, Dict, Any

from app.core.config import get_llm
from app.core.logger import logger


async def call_review_agent(
    role_description: str,
    guidelines: str,
    diff_text: str,
) -> List[Dict[str, Any]]:
    """
    Generic helper:
    - Builds structured prompt
    - Calls Gemini using ainvoke() (correct for LangChain v0.1.x)
    - Strips markdown code fences
    - Parses JSON safely
    """

    llm = get_llm()   # ChatGoogleGenerativeAI(model="gemini-2.0-flash" or similar)

    prompt = f"""
You are an expert code reviewer specializing in {role_description}.
You will be given a unified git diff containing ONLY changed code.

Your tasks:
- Analyze ONLY the changed hunks in the diff.
- Identify issues based on your specialization.
- For each issue, output a JSON object:
  - "file": filename
  - "line": line number if inferable, else null
  - "severity": one of ["INFO", "LOW", "MEDIUM", "HIGH"]
  - "category": uppercase label (LOGIC / READABILITY / PERFORMANCE / SECURITY)
  - "comment": explanation
  - "suggestion": optional fix

{guidelines}

STRICT RULES:
- Output MUST be ONLY a VALID JSON array.
- NO markdown, NO explanation outside JSON.
- If no issues found, return [].

Here is the diff:

{diff_text}
""".strip()

    logger.info(f"🤖 Calling agent: {role_description} ...")

    # --- LLM CALL ---
    try:
        response = await llm.ainvoke(prompt)
        response_text = response.content or ""
    except Exception as e:
        logger.error(f"LLM call failed for {role_description}: {e}")
        return []

    # --- CLEAN RAW TEXT → REMOVE CODE FENCES ---
    clean = response_text.strip()

    # Remove ```json ... ```
    clean = clean.replace("```json", "").replace("```", "").strip()

    # Remove any other fenced markdown blocks
    clean = re.sub(
        r"```.*?```", 
        lambda m: m.group(0).strip("`"), 
        clean, 
        flags=re.DOTALL
    ).strip()

    # --- JSON PARSING ---
    try:
        data = json.loads(clean)

        if isinstance(data, dict):
            data = data.get("comments", [])

        if not isinstance(data, list):
            logger.error(f"{role_description} output is not a list. Returning [].")
            return []

        return data

    except Exception as e:
        logger.error(f"❌ Failed to parse JSON from {role_description}: {e}")
        logger.error("Raw LLM Output:")
        logger.error(response_text)
        return []
