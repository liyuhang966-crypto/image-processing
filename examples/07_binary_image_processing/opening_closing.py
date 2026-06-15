"""对应章节：7.3 开运算与闭运算

运行方式：
    python 07_binary_image_processing/opening_closing.py [可选图片路径]
"""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from _common import main


if __name__ == "__main__":
    main()
