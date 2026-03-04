import re

NUMERIC_PATTERN = re.compile(
    r"(?P<value>\d+(?:,\d+)?(?:\.\d+)?)\s*(?P<unit>mm|cm|m|in|inch|ft|kg|lb|kN|N|psi|MPa|Pa|gauge)?",
    re.I
)


def extract_numeric_entities(text: str):

    entities = []

    for match in NUMERIC_PATTERN.finditer(text):

        value = match.group("value").replace(",", "")
        unit = match.group("unit")

        start = max(0, match.start() - 30)
        end = match.end() + 30

        entities.append({
            "value": float(value),
            "unit": unit,
            "context": text[start:end]
        })

    return entities