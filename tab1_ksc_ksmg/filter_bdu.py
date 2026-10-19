import re

BDU_PATTERN = re.compile(
    r'\bBDU:\d{4}-\d{4,6}\b',
    re.IGNORECASE,
)


def extract(text: str):
    return [m.upper() for m in BDU_PATTERN.findall(text)]