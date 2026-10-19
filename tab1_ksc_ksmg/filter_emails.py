import re

EMAIL_PATTERN = re.compile(
    r'\b[A-Za-z0-9._%+-]+@(?:[A-Za-z0-9-]+(?:\[\.\]|\.))+[A-Za-zА-Яа-яЁё]{2,}\b',
    re.UNICODE,
)


def extract(text: str):
    return [m.group().replace("[.]", ".") for m in EMAIL_PATTERN.finditer(text)]