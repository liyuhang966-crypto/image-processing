"""对应章节：10.2.2 哈夫曼（Huffman）编码

运行方式：
    python 10_image_compression/huffman_encoding_demo.py [可选图片路径]
"""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from _common import main


if __name__ == "__main__":
    main()
