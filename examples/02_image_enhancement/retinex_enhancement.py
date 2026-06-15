"""对应章节：2.8 Retinex 图像增强方法

运行方式：
    python 02_image_enhancement/retinex_enhancement.py [可选图片路径]
"""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from _common import main


if __name__ == "__main__":
    main()
