import re
import sys
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

from add_pdf_reading_blocks import block, remove_old_blocks


class PdfReadingBlocksTest(unittest.TestCase):
    def test_block_embeds_only_the_start_page(self):
        text = block(32, 36)

        embeds = re.findall(r"!\[\[raw/books/数字图像处理基础_朱虹\.pdf#page=(\d+)\]\]", text)

        self.assertEqual(embeds, ["32"])
        self.assertIn("PDF 页码：32-36", text)
        self.assertIn("[[raw/books/数字图像处理基础_朱虹.pdf#page=32]]", text)

    def test_block_has_repo_relative_pdf_link(self):
        text = block(32, 36)

        self.assertIn(
            "[raw/books/数字图像处理基础_朱虹.pdf#page=32](../../raw/books/数字图像处理基础_朱虹.pdf#page=32)",
            text,
        )
        self.assertIn("GitHub/文件内", text)

    def test_remove_old_blocks_preserves_note_body(self):
        text = """# 2.1 γ校正

> [!note] 书中对应页
> PDF 页码：32-36
> 打开原页：[[raw/books/数字图像处理基础_朱虹.pdf#page=32]]
> ![[raw/books/数字图像处理基础_朱虹.pdf#page=32]]

## 来源

* 书名：数字图像处理基础

## 核心概念

这里是正文。
"""

        cleaned = remove_old_blocks(text)

        self.assertNotIn("[!note] 书中对应页", cleaned)
        self.assertIn("## 来源", cleaned)
        self.assertIn("## 核心概念", cleaned)
        self.assertIn("这里是正文。", cleaned)


if __name__ == "__main__":
    unittest.main()
