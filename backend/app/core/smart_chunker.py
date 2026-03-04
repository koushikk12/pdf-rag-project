from typing import List, Dict


MAX_PARAGRAPH_TOKENS = 500   # safe size for embedding
MIN_PARAGRAPH_LENGTH = 40


def estimate_tokens(text: str) -> int:
    # Rough token estimate (good enough for chunking)
    return len(text.split())


def build_chunk(blocks: List[Dict]) -> Dict:
    return {
        "text": " ".join(b["text"].strip() for b in blocks),
        "page": blocks[0]["page"],
        "block_type": blocks[0]["type"],
    }


def smart_chunk_blocks(blocks: List[Dict]) -> List[Dict]:

    chunks = []
    current_chunk = []
    current_tokens = 0
    current_page = None
    current_type = None

    for block in blocks:

        text = block["text"].strip()
        block_type = block["type"]
        page = block["page"]
        tokens = estimate_tokens(text)

        # 🔴 RULE 1: Never cross page boundary
        if current_page is not None and page != current_page:
            if current_chunk:
                chunks.append(build_chunk(current_chunk))
            current_chunk = []
            current_tokens = 0

        # 🔴 RULE 2: Never mix block types
        if current_type is not None and block_type != current_type:
            if current_chunk:
                chunks.append(build_chunk(current_chunk))
            current_chunk = []
            current_tokens = 0

        # 🔴 RULE 3: Headers always standalone chunks
        if block_type == "header":
            if current_chunk:
                chunks.append(build_chunk(current_chunk))
            chunks.append({
                "text": text,
                "page": page,
                "block_type": "header"
            })
            current_chunk = []
            current_tokens = 0
            current_page = page
            current_type = None
            continue

        # 🔴 RULE 4: Table rows = individual chunks
        if block_type == "table_row":
            if current_chunk:
                chunks.append(build_chunk(current_chunk))
                current_chunk = []
                current_tokens = 0

            chunks.append({
                "text": text,
                "page": page,
                "block_type": "table_row"
            })

            current_page = page
            current_type = None
            continue

        # 🔴 RULE 5: Drawing labels = atomic
        if block_type == "drawing_label" or block_type == "short_text":
            if current_chunk:
                chunks.append(build_chunk(current_chunk))
                current_chunk = []
                current_tokens = 0

            chunks.append({
                "text": text,
                "page": page,
                "block_type": block_type
            })

            current_page = page
            current_type = None
            continue

        # 🔵 RULE 6: Paragraph grouping (semantic size control)
        if block_type == "paragraph":
            if current_tokens + tokens > MAX_PARAGRAPH_TOKENS and current_chunk:
                chunks.append(build_chunk(current_chunk))
                current_chunk = []
                current_tokens = 0

            current_chunk.append(block)
            current_tokens += tokens
            current_page = page
            current_type = block_type
            continue

    # Add leftover chunk
    if current_chunk:
        chunks.append(build_chunk(current_chunk))

    return chunks