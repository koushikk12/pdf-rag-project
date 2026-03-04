from app.core.section_detector import detect_section


def build_structured_blocks(pages):

    sections = []
    current_section = {
        "section_code": "0",
        "section_title": "Introduction",
        "blocks": []
    }

    for page in pages:

        page_number = page["page_number"]
        text = page.get("text", "")

        lines = text.split("\n")

        for line in lines:

            line = line.strip()

            if not line:
                continue

            section = detect_section(line)

            if section:

                sections.append(current_section)

                current_section = {
                    "section_code": section["section_code"],
                    "section_title": section["section_title"],
                    "blocks": []
                }

                continue

            current_section["blocks"].append({
                "text": line,
                "page": page_number,
                "type": "paragraph"
            })

    sections.append(current_section)

    return sections