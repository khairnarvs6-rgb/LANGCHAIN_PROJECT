from langchain_groq import ChatGroq

from app.config import GROQ_API_KEY, GROQ_MODEL


def get_llm():
    """Create and return the Groq chat model."""

    if not GROQ_API_KEY:
        raise RuntimeError(
            "GROQ_API_KEY is missing. Add it to your .env file."
        )

    if not GROQ_MODEL:
        raise RuntimeError(
            "GROQ_MODEL is missing. Set a supported model in .env."
        )

    return ChatGroq(
        model=GROQ_MODEL,
        temperature=0,
    )