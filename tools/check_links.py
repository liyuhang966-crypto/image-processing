"""Check wiki links and local media references.

The original PDF is intentionally absent from the public repository. Links to
raw/books/*.pdf are allowed only as local Obsidian reading blocks.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path


WIKI_LINK_RE = re.compile(r"\[\[([^\]#|]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]")
MARKDOWN_LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
ALLOWED_MISSING_PREFIXES = ("raw/books/", "../raw/books/", "../../raw/books/")


def note_index(wiki_dir: Path) -> set[str]:
    index: set[str] = set()
    for path in wiki_dir.rglob("*.md"):
        rel = path.relative_to(wiki_dir.parent).as_posix()
        index.add(rel)
        index.add(rel.removesuffix(".md"))
        index.add(path.stem)
        index.add(path.name)
        if path.name == "README.md":
            index.add(path.parent.name)
    return index


def is_allowed_pdf_reference(target: str) -> bool:
    normalized = target.replace("\\", "/")
    return normalized.endswith(".pdf") or ".pdf#page=" in normalized or any(
        normalized.startswith(prefix) for prefix in ALLOWED_MISSING_PREFIXES
    )


def resolve_markdown_target(source: Path, target: str) -> Path | None:
    target = target.split("#", 1)[0].strip()
    if not target or "://" in target or target.startswith("mailto:"):
        return None
    if is_allowed_pdf_reference(target):
        return None
    return (source.parent / target).resolve()


def main() -> int:
    root = Path.cwd()
    wiki_dir = root / "wiki"
    known_notes = note_index(wiki_dir)
    errors: list[str] = []

    markdown_files = [root / "README.md", root / "index.md", root / "coverage_report.md"]
    markdown_files.extend(sorted(wiki_dir.rglob("*.md")))
    markdown_files.extend(sorted((root / "graph").glob("*.md")))

    for path in markdown_files:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        for raw in WIKI_LINK_RE.findall(text):
            target = raw.strip().replace("\\", "/")
            if is_allowed_pdf_reference(target):
                continue
            candidates = {target, target.removesuffix(".md"), Path(target).name, Path(target).stem}
            if not candidates & known_notes:
                errors.append(f"{path.relative_to(root)}: unresolved wiki link [[{raw}]]")

        for raw in MARKDOWN_LINK_RE.findall(text):
            resolved = resolve_markdown_target(path, raw)
            if resolved and not resolved.exists():
                errors.append(f"{path.relative_to(root)}: missing local link {raw}")

    if errors:
        print("Link check failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Link check passed for {len(markdown_files)} Markdown files.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
