from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from app.rag import ask_question
from app.vector_store import index_documents


app = FastAPI(
    title="LangChain Groq RAG API",
    description="Ask questions about your own documents.",
    version="1.0.0",
)


class QuestionRequest(BaseModel):
    question: str = Field(
        min_length=1,
        max_length=2000,
    )


@app.get("/")
def home():
    return {"message": "LangChain Groq RAG API is running."}


@app.post("/ingest")
def ingest():
    try:
        index_documents()
        return {"message": "Documents indexed successfully."}
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc


@app.post("/ask")
def ask(request: QuestionRequest):
    try:
        return ask_question(request.question)
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc