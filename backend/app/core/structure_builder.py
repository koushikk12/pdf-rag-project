def build_structured_blocks(layout_elements):

    structured_blocks = []

    for element in layout_elements:

        block_type = element["type"].lower()
        text = element["text"].strip()

        if not text:
            continue

        if block_type in ["title"]:
            block_type = "header"

        elif block_type in ["narrativetext", "text"]:
            block_type = "text"

        elif block_type in ["table"]:
            block_type = "table"

        elif block_type in ["figure", "image"]:
            block_type = "diagram"

        structured_blocks.append({
            "type": block_type,
            "text": text,
            "page": element.get("page", None)
        })

    return structured_blocks