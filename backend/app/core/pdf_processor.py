import fitz
from PIL import Image
import pytesseract
import io


def ocr_page(page, dpi=400):
    pix = page.get_pixmap(dpi=dpi)
    img = Image.open(io.BytesIO(pix.tobytes()))
    return pytesseract.image_to_string(img)


def detect_if_any_page_scanned(doc):
    for page in doc:
        native_text = page.get_text().strip()

        # If very little selectable text → consider scanned
        if len(native_text) < 20:
            return True

    return False


def extract_text_from_pdf(file_path):
    doc = fitz.open(file_path)

    force_ocr = detect_if_any_page_scanned(doc)

    pages = []

    for page_number, page in enumerate(doc):

        if force_ocr:
            text = ocr_page(page)
            source = "forced_full_document_ocr"
        else:
            text = page.get_text()
            source = "native"

        pages.append({
            "page_number": page_number + 1,
            "extraction_source": source,
            "text": text
        })

    return pages