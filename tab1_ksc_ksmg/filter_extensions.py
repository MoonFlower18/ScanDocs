import re

EXT_CHAIN_PATTERN = re.compile(r'(?:\.[A-Za-z0-9]{2,8})+')

# Доменные зоны, которые НЕ считаем расширениями СНЕСТИ В СЛОВАРЬ
TLD_EXCLUDE = {"ru", "com"}


def extract(text: str):
    results = []
    for m in EXT_CHAIN_PATTERN.finditer(text):
        candidate = m.group()
        parts = [p for p in candidate.split(".") if p]

        if all(p.lower() in TLD_EXCLUDE for p in parts):
            continue
        if not any(any(c.isalpha() for c in p) for p in parts):
            continue

        results.append(candidate)
    return results