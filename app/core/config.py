from langchain_google_genai import ChatGoogleGenerativeAI
from app.core.settings import settings


def get_llm():
    """
    Returns a Gemini chat model wrapped for LangChain.
    No imports from agents here! Avoid circular imports.
    """
    if not settings.GEMINI_API_KEY:
        raise RuntimeError("GEMINI_API_KEY is not set in environment.")

    return ChatGoogleGenerativeAI(
        model=settings.GEMINI_MODEL_NAME,
        google_api_key=settings.GEMINI_API_KEY,
        temperature=0.1,
    )
