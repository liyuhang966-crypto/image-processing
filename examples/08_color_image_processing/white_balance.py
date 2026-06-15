"""对应章节：8.3.1 白平衡法

运行方式：
    python 08_color_image_processing/white_balance.py [可选图片路径]
"""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from _common import main


if __name__ == "__main__":
    main()
