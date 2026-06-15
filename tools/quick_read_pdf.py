from __future__ import annotations

import json
import os
import shutil
from pathlib import Path

import fitz


ROOT = Path(__file__).resolve().parents[1]
SOURCE_PDF = Path(r"C:\Users\lizi\Desktop\学习\数字图像处理基础 (朱虹)(1).pdf")
PROJECT_PDF = ROOT / "raw" / "books" / "数字图像处理基础_朱虹.pdf"
OFFSET = 15


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def prepare_pdf() -> str:
    PROJECT_PDF.parent.mkdir(parents=True, exist_ok=True)
    if PROJECT_PDF.exists() or PROJECT_PDF.is_symlink():
        return "existing"
    try:
        os.link(SOURCE_PDF, PROJECT_PDF)
        return "hardlink"
    except OSError:
        pass
    try:
        PROJECT_PDF.symlink_to(SOURCE_PDF)
        return "symlink"
    except OSError:
        shutil.copy2(SOURCE_PDF, PROJECT_PDF)
        return "copy"


def extract_range(doc: fitz.Document, start_pdf: int, end_pdf: int) -> str:
    chunks: list[str] = []
    for page in range(start_pdf, end_pdf + 1):
        book_page = page - OFFSET if page > OFFSET else "front-matter"
        text = doc.load_page(page - 1).get_text("text").strip()
        chunks.append(f"\n\n<!-- PDF_PAGE {page}; BOOK_PAGE {book_page} -->\n\n{text}")
    return "".join(chunks).strip() + "\n"


def main() -> None:
    for folder in [
        "raw/books",
        "raw/extracted_text",
        "raw/temp",
        "wiki/01_引言",
        "wiki/02_图像增强",
        "wiki/98_习题索引",
        "assets/extracted_figures",
        "assets/sample_images",
        "graph",
        "tools",
        "templates",
    ]:
        (ROOT / folder).mkdir(parents=True, exist_ok=True)

    pdf_method = prepare_pdf()
    doc = fitz.open(SOURCE_PDF)
    toc = doc.get_toc(simple=True)

    write(ROOT / "raw/extracted_text/ch01_引言.md", extract_range(doc, 16, 30))
    write(ROOT / "raw/extracted_text/ch02_图像增强_preview.md", extract_range(doc, 31, 56))

    sections = [
        ("1.1", "数字图像处理、计算机视觉、计算机图形学", 18, 3),
        ("1.2", "数字图像处理系统的结构", 20, 5),
        ("1.3", "数字图像的基本概念", 21, 6),
        ("1.3.1", "数字图像的数值描述", 21, 6),
        ("1.3.2", "数字图像的灰度直方图", 24, 9),
        ("1.4", "数字图像处理的主要研究内容", 27, 12),
        ("1.5", "本书的结构安排", 29, 14),
        ("1.x", "习题", 30, 15),
        ("2.1", "γ校正", 32, 18),
        ("2.2", "对比度线性展宽", 37, 23),
        ("2.5", "直方图均衡化", 46, 32),
    ]
    page_map = {
        "book": "数字图像处理基础",
        "author": "朱虹",
        "pdf_total_pages": doc.page_count,
        "source_pdf": str(SOURCE_PDF),
        "project_pdf": "raw/books/数字图像处理基础_朱虹.pdf",
        "pdf_storage_method": pdf_method,
        "book_to_pdf_offset": OFFSET,
        "rule": "PDF 页码 = 书中页码 + 15；例如书中第 1 页在 PDF 第 16 页。",
        "status": "已根据内置目录和页面文本初步确认；后续章节仍建议抽样复核",
        "sections": [
            {"number": n, "title": t, "pdf_page": p, "book_page": b}
            for n, t, p, b in sections
        ],
    }
    write(ROOT / "page_map.json", json.dumps(page_map, ensure_ascii=False, indent=2) + "\n")

    write(
        ROOT / "source_manifest.md",
        f"""# 来源清单

| 字段 | 内容 |
|---|---|
| 书名 | 数字图像处理基础 |
| 作者 | 朱虹 |
| 原始路径 | `{SOURCE_PDF}` |
| 项目内路径 | `raw/books/数字图像处理基础_朱虹.pdf` |
| PDF 页数 | {doc.page_count} |
| 内置目录项 | {len(toc)} |
| 项目内 PDF 准备方式 | {pdf_method} |
| 存储说明 | 优先使用链接以减少本地空间压力；`raw/books/*` 默认不提交。 |
""",
    )
    write(
        ROOT / "extraction_log.md",
        f"""# 抽取日志

- 成功读取源 PDF：是
- PDF 总页数：{doc.page_count}
- 内置目录项数量：{len(toc)}
- 页码关系：PDF 页码 = 书中页码 + 15
- 已抽取中间文本：`raw/extracted_text/ch01_引言.md`、`raw/extracted_text/ch02_图像增强_preview.md`
- 图片抽取：暂未执行；为节省空间，后续只提取被 wiki 引用的教学图。
- 公式识别：需人工复核。
""",
    )
    write(
        ROOT / ".gitignore",
        """.venv/
__pycache__/
**/__pycache__/
.pytest_cache/
.obsidian/
raw/books/*
!raw/books/README.md
raw/temp/
*.tmp
*.log
.DS_Store
Thumbs.db
data/processed/*.json
""",
    )
    write(
        ROOT / "raw/books/README.md",
        "# 原始书籍目录\n\n这里保存处理用 PDF 副本或链接。PDF 默认被 `.gitignore` 忽略，不上传。\n",
    )
    write(
        ROOT / "requirements.txt",
        "pymupdf\npillow\nnumpy\nmatplotlib\nopencv-python\nnetworkx\nPyWavelets\n",
    )

    print(
        json.dumps(
            {
                "pages": doc.page_count,
                "toc": len(toc),
                "offset": OFFSET,
                "pdf_method": pdf_method,
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
