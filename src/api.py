import sys
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parent

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from agents import ask_agent

app = FastAPI(
    title="Bhagavad Gita Agentic RAG",
    description=(
        "Agentic RAG API using CrewAI, "
        "Ollama and PGVector"
    ),
    version="1.0.0",
)

class QuestionRequest(BaseModel):

    question: str

class AnswerResponse(BaseModel):

    question: str
    answer: str

@app.get("/")
def root():

    return {
        "application": "Bhagavad Gita Agentic RAG",
        "status": "running",
        "version": "1.0.0",
    }

@app.get("/health")
def health():

    return {
        "status": "healthy"
    }

@app.post(
    "/ask",
    response_model=AnswerResponse,
)
def ask_question(
    request: QuestionRequest,
):

    question = request.question.strip()

    if not question:

        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty.",
        )

    try:

        answer = ask_agent(
            question
        )

        return AnswerResponse(
            question=question,
            answer=answer,
        )

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error),
        )

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        "api:app",
        host="127.0.0.1",
        port=8000,
        reload=False,
    )