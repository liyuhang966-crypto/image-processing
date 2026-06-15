"""对应章节：4.5 非局部均值滤波

运行方式：
    python 04_image_denoising/non_local_means_filter.py [可选图片路径]
"""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from _common import main


if __name__ == "__main__":
    main()
