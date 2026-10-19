import os
import re


# Формат имени: ФСТЭК N 240 83 1983 от 09.10.2026.docx
DATESTAMP_PATTERN = re.compile(
    r'(?:ФСТЭК N[ \s]+)?'        # префикс
    r'(.+?)'                     # номер приказа
    r'[ \s]+от[ \s]+'            # разделитель «от»
    r'(\d{2}\.\d{2}\.\d{4})',    # дата
    re.IGNORECASE,
)


def extract_datestamp(filepath: str) -> str:
    if not filepath:
        return ""

    basename = os.path.splitext(os.path.basename(filepath))[0]
    m = DATESTAMP_PATTERN.search(basename)

    if not m:
        return ""

    number_part = m.group(1).replace("_", " ").strip()
    date_part = m.group(2)
    return f"{number_part} от {date_part}"