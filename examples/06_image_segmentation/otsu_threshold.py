"""对应章节：6.1.3 最大类间、类内方差比法

运行方式：
    python 06_image_segmentation/otsu_threshold.py [可选图片路径]
"""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from _common import main


if __name__ == "__main__":
    main()
