"""对应章节：5.6 LOG 滤波算法

运行方式：
    python 05_image_sharpening/log_filter.py [可选图片路径]
"""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from _common import main


if __name__ == "__main__":
    main()
