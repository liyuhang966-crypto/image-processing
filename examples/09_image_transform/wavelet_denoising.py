"""对应章节：9.3.4 应用于图像去噪

运行方式：
    python 09_image_transform/wavelet_denoising.py [可选图片路径]
"""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from _common import main


if __name__ == "__main__":
    main()
