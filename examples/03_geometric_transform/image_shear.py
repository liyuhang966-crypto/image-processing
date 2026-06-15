"""对应章节：3.2.3 图像的错切

运行方式：
    python 03_geometric_transform/image_shear.py [可选图片路径]
"""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from _common import main


if __name__ == "__main__":
    main()
