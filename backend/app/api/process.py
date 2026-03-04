from fastapi import APIRouter
import os
import json

from app.core.pdf_processor import extract_text_from_pdf
from app.core.structure_builder import build_structured_blocks

router = APIRouter()

UPLOAD_DIR = "storage/uploads"
DEBUG_FILE = "storage/structured_debug.json"


@router.post("/process/{filename}")
def process_pdf(filename: str):

    file_path = os.path.join(UPLOAD_DIR, filename)

    if not os.path.exists(file_path):
        return {"error": "File not found"}

    print("\n===== START PROCESSING =====")

    # 1️⃣ Extract text
    pages = extract_text_from_pdf(file_path)

    print(f"Pages extracted: {len(pages)}")

    # 2️⃣ Build sections
    sections = build_structured_blocks(pages)

    print(f"Sections detected: {len(sections)}")

    # 3️⃣ Save debug output
    os.makedirs("storage", exist_ok=True)

    with open(DEBUG_FILE, "w", encoding="utf-8") as f:
        json.dump(sections, f, indent=2)

    print(f"\nStructured output saved to: {DEBUG_FILE}")

    return {
        "message": "Builder debug completed",
        "pages_extracted": len(pages),
        "sections_detected": len(sections),
        "debug_file": DEBUG_FILE
    }