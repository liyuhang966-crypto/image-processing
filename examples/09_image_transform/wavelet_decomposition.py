"""对应章节：9.2.3 小波的多尺度分解与重构

运行方式：
    python 09_image_transform/wavelet_decomposition.py [可选图片路径]
"""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from _common import main


if __name__ == "__main__":
    main()
