from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
)
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.config import (
    CHUNK_OVERLAP,
    CHUNK_SIZE,
    DOCUMENTS_DIR,
)


def load_documents():
    """Load all supported PDF and TXT files."""

    documents = []

    DOCUMENTS_DIR.mkdir(parents=True, exist_ok=True)

    for file_path in DOCUMENTS_DIR.iterdir():
        if file_path.suffix.lower() == ".pdf":
            loader = PyPDFLoader(str(file_path))
        elif file_path.suffix.lower() == ".txt":
            loader = TextLoader(
                str(file_path),
                encoding="utf-8",
            )
        else:
            continue

        documents.extend(loader.load())

    return documents


def split_documents(documents):
    """Split loaded documents into smaller chunks."""

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        add_start_index=True,
    )

    return splitter.split_documents(documents)


if __name__ == "__main__":
    docs = load_documents()
    chunks = split_documents(docs)

    print(f"Loaded documents/pages: {len(docs)}")
    print(f"Generated chunks: {len(chunks)}")

    if chunks:
        print("\nFirst chunk:")
        print(chunks[0].page_content[:500])
        print("\nMetadata:")
        print(chunks[0].metadata)