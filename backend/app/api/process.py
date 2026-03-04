from fastapi import APIRouter
import os
import json

from app.core.pdf_processor import extract_text_from_pdf
from app.core.structure_builder import build_structured_blocks
from app.core.smart_chunker import smart_chunk_blocks
from app.core.embedding_service import embed_chunks, store_in_faiss

router = APIRouter()

UPLOAD_DIR = "storage/uploads"
DEBUG_OUTPUT_PATH = "storage/structured_debug.json"


@router.post("/process/{filename}")
def process_pdf(filename: str):

    file_path = os.path.join(UPLOAD_DIR, filename)

    if not os.path.exists(file_path):
        return {"error": "File not found"}

    # 1️⃣ Extract text
    pages = extract_text_from_pdf(file_path)

    print("\n===== TOTAL PAGES EXTRACTED =====")
    print(len(pages))

    # 2️⃣ Build structured blocks
    structured_blocks = build_structured_blocks(pages)

    print("\n===== TOTAL STRUCTURED BLOCKS =====")
    print(len(structured_blocks))

    # 3️⃣ Save FULL structured output for inspection
    os.makedirs("storage", exist_ok=True)

    with open(DEBUG_OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(structured_blocks, f, indent=2, ensure_ascii=False)

    print(f"\n===== STRUCTURE SAVED TO {DEBUG_OUTPUT_PATH} =====\n")

    # 4️⃣ Continue normal pipeline
    chunks = smart_chunk_blocks(structured_blocks)

    if not chunks:
        return {"error": "No chunks generated"}

    embeddings = embed_chunks(chunks)
    store_in_faiss(chunks, embeddings)

    return {
        "message": "Document processed successfully",
        "total_pages": len(pages),
        "total_blocks": len(structured_blocks),
        "total_chunks": len(chunks),
        "debug_file": DEBUG_OUTPUT_PATH
    }