from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from app.llm import get_llm
from app.vector_store import get_vector_store


prompt = ChatPromptTemplate.from_template(
    """
You are a helpful assistant answering questions from supplied documents.

Use the context below to answer the question.
If the context does not contain the answer, say that you
could not find sufficient information in the documents.

Context:
{context}

Question:
{question}

Answer:
"""
)


def ask_question(question: str):
    """Retrieve relevant chunks and generate a grounded answer."""

    vector_store = get_vector_store()

    # Search for the three most relevant chunks.
    retriever = vector_store.as_retriever(
        search_kwargs={"k": 3}
    )

    docs = retriever.invoke(question)

    if not docs:
        return {
            "answer": "No relevant information was found.",
            "sources": [],
        }

    context = "\n\n".join(
        f"Source: {doc.metadata.get('source', 'unknown')}\n"
        f"Content: {doc.page_content}"
        for doc in docs
    )

    chain = prompt | get_llm() | StrOutputParser()

    answer = chain.invoke(
        {
            "context": context,
            "question": question,
        }
    )

    sources = [
        {
            "source": doc.metadata.get("source", "unknown"),
            "page": doc.metadata.get("page"),
            "content_preview": doc.page_content[:200],
        }
        for doc in docs
    ]

    return {
        "answer": answer,
        "sources": sources,
    }


if __name__ == "__main__":
    question = input("Ask a question about your documents: ")
    result = ask_question(question)

    print("\nAnswer:")
    print(result["answer"])

    print("\nRetrieved sources:")
    for source in result["sources"]:
        print(source)