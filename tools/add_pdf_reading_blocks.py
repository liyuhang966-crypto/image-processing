from __future__ import annotations

from pathlib import Path

import fitz

from build_full_knowledge_base import PDF, build_entries, entry_path


PDF_VAULT_PATH = "raw/books/数字图像处理基础_朱虹.pdf"


def block(pdf_page: int, end_pdf_page: int) -> str:
    page_range = f"{pdf_page}-{end_pdf_page}" if end_pdf_page > pdf_page else str(pdf_page)
    lines = [
        "> [!note] 书中对应页",
        f"> PDF 页码：{page_range}",
        f"> 打开原页（Obsidian）：[[{PDF_VAULT_PATH}#page={pdf_page}]]",
        ">",
        "> GitHub 公开仓库不随附原书 PDF；下载仓库后，将有权使用的同名 PDF 放入 `raw/books/`，下面的 Obsidian 本地内嵌预览才会显示。",
        f"> ![[{PDF_VAULT_PATH}#page={pdf_page}]]",
    ]
    return "\n".join(lines)


def remove_old_blocks(text: str) -> str:
    # Remove only the contiguous blockquote callout lines; never scan across body headings.
    lines = text.splitlines()
    cleaned: list[str] = []
    index = 0
    while index < len(lines):
        if lines[index].strip() in {"> [!note] 书中对应页", "> [!note] 书中原页"}:
            while cleaned and cleaned[-1] == "":
                cleaned.pop()
            index += 1
            while index < len(lines) and lines[index].startswith(">"):
                index += 1
            while index < len(lines) and lines[index] == "":
                index += 1
            if cleaned and index < len(lines):
                cleaned.append("")
            continue
        cleaned.append(lines[index])
        index += 1
    return "\n".join(cleaned).strip() + "\n"


def add_block(path: Path, pdf_page: int, end_pdf_page: int) -> None:
    text = remove_old_blocks(path.read_text(encoding="utf-8"))
    lines = text.splitlines()
    if lines and lines[0].startswith("# "):
        new_text = "\n".join([lines[0], "", block(pdf_page, end_pdf_page), "", *lines[1:]])
    else:
        new_text = block(pdf_page, end_pdf_page) + "\n\n" + text
    path.write_text(new_text.replace("\n\n\n", "\n\n"), encoding="utf-8", newline="\n")


def main() -> None:
    entries = build_entries(fitz.open(PDF))
    updated = 0
    for entry in entries:
        if entry["kind"] not in {"section", "reference"}:
            continue
        path = entry_path(entry)
        if path.exists():
            add_block(path, entry["pdf_page"], entry["end_pdf_page"])
            updated += 1
    print({"updated": updated})


if __name__ == "__main__":
    main()
