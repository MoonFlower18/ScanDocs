import re

URL_PATTERN = re.compile(
    r'\b(?:[A-Za-zА-Яа-яЁё0-9_-]+(?:\[\.\]|\.))+[A-Za-zА-Яа-яЁё]{2,}\b'
)

IP_PATTERN = re.compile(
    r'\b(?:\d{1,3}(?:\[\.\]|\.)){3}\d{1,3}\b'
)


def _normalize(text: str) -> str:
    return text.replace("[.]", ".")


def extract(text: str):
    results = []

    for m in URL_PATTERN.finditer(text):
        results.append(_normalize(m.group()))

    for m in IP_PATTERN.finditer(text):
        ip = _normalize(m.group())
        parts = ip.split(".")
        if len(parts) == 4 and all(0 <= int(p) <= 255 for p in parts):
            results.append(ip)

    return results