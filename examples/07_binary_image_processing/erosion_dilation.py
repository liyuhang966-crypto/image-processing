"""对应章节：7.2 腐蚀与膨胀

运行方式：
    python 07_binary_image_processing/erosion_dilation.py [可选图片路径]
"""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from _common import main


if __name__ == "__main__":
    main()
