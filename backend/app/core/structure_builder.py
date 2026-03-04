import re

SECTION_PATTERN = re.compile(r"^(\d+(\.\d+)*)\s+(.*)")


def build_structured_blocks(pages):

    sections = []
    current_section = None

    for page in pages:

        lines = page["text"].split("\n")

        for line in lines:

            line = line.strip()
            if not line:
                continue

            match = SECTION_PATTERN.match(line)

            # If a new section starts
            if match:

                if current_section:
                    sections.append(current_section)

                current_section = {
                    "section_code": match.group(1),
                    "section_title": match.group(3),
                    "text": "",
                    "page": page["page_number"]
                }

            else:

                if current_section:
                    current_section["text"] += " " + line
                else:
                    # Text before first section
                    current_section = {
                        "section_code": "intro",
                        "section_title": "Introduction",
                        "text": line,
                        "page": page["page_number"]
                    }

    if current_section:
        sections.append(current_section)

    return sections