"""对应章节：2.3 灰级窗与灰级窗切片

运行方式：
    python 02_image_enhancement/gray_level_window.py [可选图片路径]
"""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from _common import main


if __name__ == "__main__":
    main()
