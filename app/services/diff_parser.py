from app.core.logger import logger

def parse_diff(diff_text: str):
    """
    Parse unified diff and return structured chunks.
    """
    logger.info("Parsing diff...")

    # full logic added in phase 2
    return [{"filename": "unknown", "patch": diff_text}]
