from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

from app.config import (
    CHROMA_DIR,
    DOCUMENTS_DIR,
    EMBEDDING_MODEL,
)
from app.documents import load_documents, split_documents


def get_embeddings():
    """Load a local sentence-embedding model."""

    return HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )


def get_vector_store():
    """Open or create the persistent Chroma collection."""

    CHROMA_DIR.mkdir(parents=True, exist_ok=True)

    return Chroma(
        collection_name="knowledge_base",
        persist_directory=str(CHROMA_DIR),
        embedding_function=get_embeddings(),
    )


def index_documents():
    """Load files, split them, and add chunks to Chroma."""

    documents = load_documents()

    if not documents:
        raise ValueError(
            f"No PDF or TXT files found in {DOCUMENTS_DIR}"
        )

    chunks = split_documents(documents)
    vector_store = get_vector_store()

    vector_store.add_documents(chunks)

    print(f"Loaded {len(documents)} document/page records.")
    print(f"Added {len(chunks)} chunks to ChromaDB.")
    print(f"Database location: {CHROMA_DIR}")


if __name__ == "__main__":
    index_documents()