from fastapi import APIRouter
import os

from app.core.pdf_processor import extract_text_from_pdf
from app.core.structure_builder import build_structured_blocks
from app.core.smart_chunker import build_chunks
from app.core.embedding_service import embed_chunks
from app.core.vector_store import build_index

router = APIRouter()

UPLOAD_DIR = "storage/uploads"


@router.post("/process/{filename}")
def process_pdf(filename: str):

    file_path = os.path.join(UPLOAD_DIR, filename)

    pages = extract_text_from_pdf(file_path)

    sections = build_structured_blocks(pages)

    chunks = build_chunks(sections)

    embeddings = embed_chunks(chunks)

    build_index(embeddings, chunks)

    return {
        "pages": len(pages),
        "sections": len(sections),
        "chunks": len(chunks),
        "message": "Document indexed successfully"
    }