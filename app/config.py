import os
from pathlib import Path

from dotenv import load_dotenv

# Project root is the parent of the app directory.
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Load environment variables from the project root.
load_dotenv(PROJECT_ROOT / ".env")

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL")

EMBEDDING_MODEL = os.getenv(
    "EMBEDDING_MODEL",
    "sentence-transformers/all-MiniLM-L6-v2",
)

DOCUMENTS_DIR = PROJECT_ROOT / "data" / "documents"
CHROMA_DIR = PROJECT_ROOT / "chroma_db"

CHUNK_SIZE = 800
CHUNK_OVERLAP = 150