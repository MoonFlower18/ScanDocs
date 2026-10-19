import re

SHA256_PATTERN = re.compile(
    r'(?<![a-fA-F0-9])[a-fA-F0-9]{64}(?![a-fA-F0-9])'
)


def extract(text: str):
    return SHA256_PATTERN.findall(text)