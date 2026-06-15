from __future__ import annotations

import re
from pathlib import Path

import fitz

from build_full_knowledge_base import PDF, ROOT, build_entries, entry_path


PDF_VAULT_PATH = "raw/books/数字图像处理基础_朱虹.pdf"


FORMULA_UPDATES = {
    "2.1": """常用幂律关系可写为：

```math
s = c r^{\\gamma}
```

其中 `r` 是输入灰度，`s` 是输出灰度，`c` 是比例常数，`\\gamma` 控制曲线形状。若要抵消设备的非线性响应，通常使用反向幂律进行校正。书中符号和归一化范围需人工复核。
""",
    "2.2": """线性对比度展宽通常使用分段线性映射：

```math
g =
\\begin{cases}
\\alpha f, & 0 \\le f < f_a \\\\
\\beta(f-f_a)+g_a, & f_a \\le f < f_b \\\\
\\gamma(f-f_b)+g_b, & f_b \\le f \\le 255
\\end{cases}
```

核心是让重要灰度区间的斜率大于 1，非重要区间的斜率小于 1。具体端点和书中公式需人工复核。
""",
    "2.5": """灰度直方图和累计分布可写为：

```math
p_r(r_k)=\\frac{n_k}{MN}
```

```math
s_k=(L-1)\\sum_{j=0}^{k}p_r(r_j)
```

其中 `n_k` 是灰度级 `r_k` 的像素数，`M N` 是图像总像素数，`L` 是灰度级数。书中具体记号需人工复核。
""",
    "3.1.1": """平移可用齐次坐标矩阵表示：

```math
\\begin{bmatrix}x'\\\\y'\\\\1\\end{bmatrix}
=
\\begin{bmatrix}1&0&t_x\\\\0&1&t_y\\\\0&0&1\\end{bmatrix}
\\begin{bmatrix}x\\\\y\\\\1\\end{bmatrix}
```
""",
    "3.1.3": """绕原点旋转的常见形式：

```math
\\begin{bmatrix}x'\\\\y'\\end{bmatrix}
=
\\begin{bmatrix}\\cos\\theta&-\\sin\\theta\\\\\\sin\\theta&\\cos\\theta\\end{bmatrix}
\\begin{bmatrix}x\\\\y\\end{bmatrix}
```

绕图像中心旋转时还需要平移到中心、旋转、再平移回去。
""",
    "3.3": """二维仿射变换可写为：

```math
\\begin{bmatrix}x'\\\\y'\\\\1\\end{bmatrix}
=
\\begin{bmatrix}a&b&t_x\\\\c&d&t_y\\\\0&0&1\\end{bmatrix}
\\begin{bmatrix}x\\\\y\\\\1\\end{bmatrix}
```

它统一表达平移、旋转、缩放、错切等线性/仿射空间变换。
""",
    "4.2": """均值滤波的典型形式：

```math
g(x,y)=\\frac{1}{|S|}\\sum_{(s,t)\\in S} f(x+s,y+t)
```

其中 `S` 是邻域窗口。它能平滑噪声，但也可能模糊边缘。
""",
    "4.3": """中值滤波使用邻域排序统计：

```math
g(x,y)=\\operatorname{median}\\{f(x+s,y+t)\\mid (s,t)\\in S\\}
```

它对椒盐噪声常比均值滤波更稳。
""",
    "5.2": """一阶微分常用于估计梯度：

```math
\\nabla f = \\left[\\frac{\\partial f}{\\partial x},\\frac{\\partial f}{\\partial y}\\right]
```

```math
|\\nabla f| \\approx \\sqrt{G_x^2+G_y^2}
```
""",
    "5.2.3": """Sobel 常用模板：

```math
G_x=
\\begin{bmatrix}
-1&0&1\\\\-2&0&2\\\\-1&0&1
\\end{bmatrix},\\quad
G_y=
\\begin{bmatrix}
-1&-2&-1\\\\0&0&0\\\\1&2&1
\\end{bmatrix}
```
""",
    "5.3.1": """Laplacian 是二阶微分算子：

```math
\\nabla^2 f = \\frac{\\partial^2 f}{\\partial x^2}+\\frac{\\partial^2 f}{\\partial y^2}
```

离散模板有多种形式，需按书中模板人工复核。
""",
    "5.5": """Canny 的核心流程是平滑、求梯度、非极大值抑制、双阈值连接。梯度幅值常写为：

```math
M(x,y)=\\sqrt{G_x^2+G_y^2}
```
""",
    "5.6": """LOG 可理解为先高斯平滑再做 Laplacian：

```math
\\nabla^2(G_\\sigma * f)
```

其中 `G_\\sigma` 是高斯核，`*` 表示卷积。
""",
    "6.1": """阈值分割的基本形式：

```math
g(x,y)=
\\begin{cases}
1, & f(x,y) \\ge T \\\\
0, & f(x,y) < T
\\end{cases}
```
""",
    "6.1.3": """Otsu 思路是选择使类间方差最大的阈值：

```math
T^*=\\arg\\max_T \\sigma_b^2(T)
```

书中称法和具体比值形式需人工复核。
""",
    "7.2.1": """腐蚀的集合表达：

```math
A\\ominus B = \\{z \\mid B_z \\subseteq A\\}
```
""",
    "7.2.2": """膨胀的集合表达：

```math
A\\oplus B = \\{z \\mid (\\hat{B})_z \\cap A \\ne \\varnothing\\}
```
""",
    "7.3.1": """开运算：

```math
A\\circ B=(A\\ominus B)\\oplus B
```
""",
    "7.3.2": """闭运算：

```math
A\\bullet B=(A\\oplus B)\\ominus B
```
""",
    "9.1.1": """一维离散傅里叶变换：

```math
F(u)=\\sum_{x=0}^{N-1} f(x)e^{-j2\\pi ux/N}
```
""",
    "9.1.2": """二维离散傅里叶变换：

```math
F(u,v)=\\sum_{x=0}^{M-1}\\sum_{y=0}^{N-1}f(x,y)e^{-j2\\pi(ux/M+vy/N)}
```
""",
    "10.2.1": """行程编码记录连续重复值：

```text
value, run_length
```

它适合长连续区域较多的图像或二值图像。
""",
    "10.2.2": """Huffman 编码的原则是高频符号用短码、低频符号用长码。平均码长可写为：

```math
\\bar{L}=\\sum_i p_i l_i
```
""",
    "11.1.1": """卷积层的输出尺寸常按下式估算：

```math
H_{out}=\\left\\lfloor\\frac{H+2P-K}{S}\\right\\rfloor+1
```

宽度方向同理，其中 `K` 为核尺寸，`P` 为填充，`S` 为步幅。
""",
}


def source_block(pdf_page: int, end_pdf_page: int) -> str:
    if end_pdf_page > pdf_page:
        page_text = f"{pdf_page}-{end_pdf_page}"
        embed = "\n".join(
            f"> ![[{PDF_VAULT_PATH}#page={page}]]"
            for page in range(pdf_page, end_pdf_page + 1)
        )
        extra = f"> 跨页范围：PDF 第 {page_text} 页，已在下方按页内嵌显示。"
    else:
        page_text = str(pdf_page)
        embed = f"> ![[{PDF_VAULT_PATH}#page={pdf_page}]]"
        extra = ""
    return f"""> [!note] 书中原页
> PDF 页码：{page_text}
> 本地 PDF：[[{PDF_VAULT_PATH}#page={pdf_page}]]
{extra}
{embed}
"""


def replace_section(text: str, heading: str, new_body: str) -> str:
    pattern = rf"## {re.escape(heading)}\n\n.*?(?=\n## |\Z)"
    replacement = f"## {heading}\n\n{new_body.strip()}\n"
    if re.search(pattern, text, flags=re.S):
        return re.sub(pattern, lambda _match: replacement, text, flags=re.S)
    return text.rstrip() + "\n\n" + replacement


def enhance_note(path: Path, number: str, pdf_page: int, end_pdf_page: int) -> bool:
    text = path.read_text(encoding="utf-8")
    block = source_block(pdf_page, end_pdf_page)
    text = re.sub(r"\n> \[!note\] 书中原页\n> PDF 页码：.*?(?=\n## |\n# |\Z)", "\n", text, flags=re.S)
    lines = text.splitlines()
    if lines and lines[0].startswith("# "):
        text = "\n".join([lines[0], "", block, *lines[1:]]).replace("\n\n\n", "\n\n")
    else:
        text = block + "\n" + text
    if number in FORMULA_UPDATES:
        text = replace_section(text, "关键公式", FORMULA_UPDATES[number])
    path.write_text(text, encoding="utf-8", newline="\n")
    return True


def main() -> None:
    doc = fitz.open(PDF)
    entries = build_entries(doc)
    touched = 0
    formula_count = 0
    for entry in entries:
        if entry["kind"] not in {"section", "reference"}:
            continue
        path = entry_path(entry)
        if not path.exists():
            continue
        enhance_note(path, entry["number"], entry["pdf_page"], entry["end_pdf_page"])
        touched += 1
        if entry["number"] in FORMULA_UPDATES:
            formula_count += 1
    print({"enhanced_notes": touched, "formula_sections": formula_count})


if __name__ == "__main__":
    main()
