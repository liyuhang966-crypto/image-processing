"""对应章节：5.2.4 Priwitt 微分算子

运行方式：
    python 05_image_sharpening/prewitt_operator.py [可选图片路径]
"""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from _common import main


if __name__ == "__main__":
    main()
