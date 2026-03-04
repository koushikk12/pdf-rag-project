from fastapi import APIRouter
import numpy as np

from app.core.embedding_service import model
from app.core.vector_store import search
from app.core.llm_service import ask_llm

router = APIRouter()


@router.post("/ask")
def ask_question(question: str):

    query_embedding = model.encode([question])

    chunks = search(np.array(query_embedding))

    context = "\n\n".join([c["text"] for c in chunks])

    answer = ask_llm(question, context)

    return {
        "answer": answer,
        "sources": chunks
    }