from __future__ import annotations

import re
from pathlib import Path

import fitz

from build_full_knowledge_base import PDF, build_entries, entry_path
from enhance_notes_with_source_refs import FORMULA_UPDATES


def replace_section(text: str, heading: str, new_body: str) -> str:
    pattern = rf"## {re.escape(heading)}\n\n.*?(?=\n## |\Z)"
    replacement = f"## {heading}\n\n{new_body.strip()}\n"
    if re.search(pattern, text, flags=re.S):
        return re.sub(pattern, lambda _match: replacement, text, flags=re.S)
    return text.rstrip() + "\n\n" + replacement


def main() -> None:
    entries = build_entries(fitz.open(PDF))
    updated = 0
    for entry in entries:
        number = entry["number"]
        if number not in FORMULA_UPDATES:
            continue
        path = entry_path(entry)
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        text = replace_section(text, "关键公式", FORMULA_UPDATES[number])
        path.write_text(text, encoding="utf-8", newline="\n")
        updated += 1
    print(f"formula_sections_updated={updated}")


if __name__ == "__main__":
    main()
