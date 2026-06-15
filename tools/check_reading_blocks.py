import re
from pathlib import Path


EMBED_PATTERN = re.compile(
    r"!\[\[raw/books/数字图像处理基础_朱虹\.pdf#page=(\d+)\]\]"
)
OPEN_PATTERN = re.compile(
    r"打开原页：\[\[raw/books/数字图像处理基础_朱虹\.pdf#page=(\d+)\]\]"
)


def reading_block(text: str) -> str | None:
    start = text.find("> [!note] 书中对应页")
    if start < 0:
        return None
    next_heading = text.find("\n## ", start)
    return text[start:] if next_heading < 0 else text[start:next_heading]


def main() -> None:
    missing = []
    invalid = []
    for path in Path("wiki").rglob("*.md"):
        if path.name in {"README.md", "00_导航.md", "99_术语表.md"}:
            continue
        text = path.read_text(encoding="utf-8")
        block = reading_block(text)
        if block is None:
            missing.append(str(path))
            continue
        embeds = EMBED_PATTERN.findall(block)
        opens = OPEN_PATTERN.findall(block)
        if len(embeds) != 1 or not opens or embeds[0] != opens[0]:
            invalid.append((str(path), opens, embeds))
    print(f"missing_reading_blocks={len(missing)}")
    print(f"invalid_reading_blocks={len(invalid)}")
    for item in missing:
        print(item)
    for item in invalid:
        print(item)
    if missing or invalid:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
