import re

SECTION_PATTERN = re.compile(r"^(\d+(\.\d+)*)\s+(.*)$")


def detect_section(text: str, font_size: float = 0):

    if font_size < 10:
        return None

    match = SECTION_PATTERN.match(text)

    if match:
        return {
            "section_code": match.group(1),
            "section_title": match.group(3)
        }

    return None