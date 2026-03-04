import re
from app.core.numeric_extractor import extract_numeric_entities


MAX_CHUNK_LENGTH = 900
MIN_CHUNK_LENGTH = 300
CHUNK_OVERLAP = 120


def normalize_text(text):

    text = text.replace("\x00", "")
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def split_long_text(text):

    parts = re.split(r"(?<=[.!?;:])\s+", text)

    chunks = []
    current = ""

    for part in parts:

        if not part:
            continue

        candidate = f"{current} {part}".strip() if current else part

        if len(candidate) <= MAX_CHUNK_LENGTH:
            current = candidate
        else:

            if current:
                chunks.append(current)

                tail = current[-CHUNK_OVERLAP:]
                current = f"{tail} {part}".strip()

            else:
                chunks.append(part[:MAX_CHUNK_LENGTH])
                current = part[MAX_CHUNK_LENGTH:]

    if current:
        chunks.append(current)

    return chunks


def build_chunks(sections):

    chunks = []

    for section in sections:

        buffer = ""

        for block in section["blocks"]:

            text = normalize_text(block["text"])

            candidate = f"{buffer} {text}".strip() if buffer else text

            if len(candidate) > MAX_CHUNK_LENGTH:

                if len(buffer) >= MIN_CHUNK_LENGTH:

                    for part in split_long_text(buffer):

                        chunks.append({
                            "text": part,
                            "section": section["section_title"],
                            "page": block["page"],
                            "numbers": extract_numeric_entities(part)
                        })

                    buffer = ""

                else:
                    buffer = candidate

            else:
                buffer = candidate

        if buffer:

            for part in split_long_text(buffer):

                chunks.append({
                    "text": part,
                    "section": section["section_title"],
                    "page": block["page"],
                    "numbers": extract_numeric_entities(part)
                })

    return chunks