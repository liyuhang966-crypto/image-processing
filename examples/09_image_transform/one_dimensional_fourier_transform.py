"""对应章节：9.1.1 一维傅里叶变换

运行方式：
    python 09_image_transform/one_dimensional_fourier_transform.py [可选图片路径]
"""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from _common import main


if __name__ == "__main__":
    main()
