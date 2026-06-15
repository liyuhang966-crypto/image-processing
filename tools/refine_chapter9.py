"""Refine chapter 9 image transform wiki, graph semantics and docs."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WIKI = ROOT / "wiki" / "09_图像变换"
EX = ROOT / "examples" / "09_image_transform"
PDF = "raw/books/数字图像处理基础_朱虹.pdf"
PDF_PAGE_NEEDS_REVIEW = 170


FILES = [
    ("9.1_图像的频域变换（傅里叶变换）.md", "9.1 图像的频域变换（傅里叶变换）", "ch09_fft_spectrum.png", "two_dimensional_fft.py", "傅里叶变换把图像从空间域映射到频域，使平滑结构、边缘细节和周期纹理以不同频率成分呈现。它适合解释滤波、频谱中心化和周期噪声。", "\\(F(u,v)=\\sum_x\\sum_y f(x,y)e^{-j2\\pi(ux/M+vy/N)}\\)", "傅里叶变换 vs 空间滤波：前者直接选择频带，后者在像素邻域操作。"),
    ("9.1.1_一维傅里叶变换.md", "9.1.1 一维傅里叶变换", "ch09_fft_spectrum.png", "one_dimensional_fourier_transform.py", "一维傅里叶变换把一行灰度信号分解成不同频率的正弦/余弦成分，可作为理解二维图像频谱的入口。", "\\(F(k)=\\sum_{n=0}^{N-1}f(n)e^{-j2\\pi kn/N}\\)", "一维傅里叶 vs 二维傅里叶：一维处理信号序列，二维处理图像平面。"),
    ("9.1.2_二维傅里叶变换.md", "9.1.2 二维傅里叶变换", "ch09_fft_spectrum.png", "two_dimensional_fft.py", "二维傅里叶变换同时分析水平和垂直方向的频率，频谱中心附近通常表示低频，远离中心表示高频细节。", "\\(F(u,v)=\\mathcal{F}\\{f(x,y)\\}\\)", "二维 FFT vs 频谱可视化：FFT 得到复数系数，可视化通常显示对数幅度谱。"),
    ("9.1.3_快速傅里叶变换（FFT）.md", "9.1.3 快速傅里叶变换（FFT）", "ch09_frequency_filtering.png", "two_dimensional_fft.py", "FFT 是傅里叶变换的快速算法，把直接计算的高复杂度降下来，使频域处理能够用于较大图像。", "\\(O(N^2)\\) 的 DFT 可由 FFT 降为约 \\(O(N\\log N)\\)。", "FFT vs DFT：数学结果等价，FFT 是高效计算方法。"),
    ("9.1.4_图像的频谱分布特性.md", "9.1.4 图像的频谱分布特性", "ch09_frequency_filtering.png", "spectrum_visualization.py", "图像频谱能显示能量分布：低频对应整体亮度和缓慢变化，高频对应边缘、纹理、噪声和细节。", "\\(|F(u,v)|\\) 常用 \\(\\log(1+|F|)\\) 压缩动态范围后显示。", "低通 vs 高通：低通保留平滑结构，高通突出细节和噪声。"),
    ("9.2_小波变换.md", "9.2 小波变换", "ch09_wavelet_multiscale.png", "wavelet_decomposition.py", "小波变换同时具有空间和尺度局部性，适合描述图像在不同分辨率下的近似和细节。", "\\(W(a,b)=\\int f(t)\\psi_{a,b}(t)dt\\)，离散形式需人工复核。", "小波 vs 傅里叶：小波有局部尺度信息，傅里叶更强调全局频率。"),
    ("9.2.1_连续小波变换.md", "9.2.1 连续小波变换", "ch09_wavelet_multiscale.png", "wavelet_decomposition.py", "连续小波通过连续尺度和平移分析信号局部结构，理论上细致但冗余较大。", "\\(\\psi_{a,b}(t)=|a|^{-1/2}\\psi((t-b)/a)\\)", "连续小波 vs 离散小波：前者更密集，后者更适合数字图像实现。"),
    ("9.2.2_离散小波变换.md", "9.2.2 离散小波变换", "ch09_wavelet_multiscale.png", "wavelet_decomposition.py", "离散小波变换用离散尺度和滤波器组把图像分解为低频近似和方向细节子带。", "\\(LL,LH,HL,HH=DWT(f)\\)", "DWT vs FFT：DWT 输出多尺度子带，FFT 输出全局频率系数。"),
    ("9.2.3_小波的多尺度分解与重构.md", "9.2.3 小波的多尺度分解与重构", "ch09_wavelet_multiscale.png", "wavelet_decomposition.py", "多尺度小波分解反复分解低频近似子带，形成从粗到细的图像表示；重构则把子带合成为原图或处理后的图像。", "\\(f\\approx IDWT(LL,LH,HL,HH)\\)", "分解 vs 重构：分解便于处理系数，重构检验处理是否保持图像结构。"),
    ("9.3_小波变换在图像处理中的应用.md", "9.3 小波变换在图像处理中的应用", "ch09_wavelet_applications.png", "wavelet_denoising.py", "小波应用通常围绕系数选择：压缩丢弃小系数，融合组合不同图像系数，增强放大细节，去噪阈值化高频系数。", "\\(\\hat{c}=T(c)\\)，其中 \\(T\\) 是量化、融合、增强或阈值函数。", "小波应用 vs 空间处理：小波先变换到多尺度系数域再处理。"),
    ("9.3.1_应用于图像压缩.md", "9.3.1 应用于图像压缩", "ch09_wavelet_applications.png", "wavelet_decomposition.py", "小波压缩利用大量高频系数较小的特点，只保留重要系数或对系数量化编码。", "压缩可抽象为：保留 \\(|c|>T\\) 的系数。", "小波压缩 vs JPEG DCT：两者都变换后量化，小波更自然支持多分辨率。"),
    ("9.3.2_应用于图像融合.md", "9.3.2 应用于图像融合", "ch09_wavelet_applications.png", "wavelet_decomposition.py", "小波融合在不同子带选择或组合多幅图像的系数，例如低频取平均，高频取绝对值较大者。", "\\(c_F=\\Phi(c_A,c_B)\\)", "融合 vs 增强：融合组合多幅图，增强处理单幅图系数。"),
    ("9.3.3_应用于图像增强.md", "9.3.3 应用于图像增强", "ch09_wavelet_applications.png", "wavelet_decomposition.py", "小波增强通过放大有用细节系数或调整不同尺度权重提升局部结构。", "\\(c'_d=\\alpha c_d\\)，其中 \\(c_d\\) 为细节系数。", "小波增强 vs 锐化：小波可按尺度选择增强，锐化多在局部差分上操作。"),
    ("9.3.4_应用于图像去噪.md", "9.3.4 应用于图像去噪", "ch09_wavelet_applications.png", "wavelet_denoising.py", "小波去噪把噪声主要视为小幅高频系数，通过软阈值或硬阈值抑制噪声后重构图像。", "\\(T_s(c)=sign(c)\\max(|c|-\\lambda,0)\\)", "小波去噪 vs 均值滤波：小波可保留部分细节，均值滤波容易模糊边缘。"),
    ("9.x_习题.md", "9.x 习题", "ch09_wavelet_applications.png", None, "本章习题应围绕空间域/频域/小波域的表示差异、频谱解释和系数处理策略展开。", "复习重点：DFT、FFT、频谱中心、小波子带、阈值去噪。", "傅里叶适合全局频率解释，小波适合局部尺度分析。"),
]


def render(item: tuple[str, str, str, str | None, str, str, str]) -> str:
    file, title, figure, code, concept, formula, compare = item
    code_line = "本节偏复习整合，无单独代码；可结合本章其他示例运行。" if code is None else f"[{code}](../../examples/09_image_transform/{code})"
    return f"""# {title}

> [!note] 书中对应页
> PDF 页码：{PDF_PAGE_NEEDS_REVIEW}
> 打开原页（Obsidian）：[[{PDF}#page={PDF_PAGE_NEEDS_REVIEW}]]
>
> GitHub 公开仓库不随附原书 PDF；下载仓库后，将有权使用的同名 PDF 放入 `raw/books/`，下面的 Obsidian 本地内嵌预览才会显示。
> ![[{PDF}#page={PDF_PAGE_NEEDS_REVIEW}]]

## 来源与状态

- 书名：数字图像处理基础
- 作者：朱虹
- 章节：第 9 章 图像变换
- 小节：{title}
- 书中页码：需人工复核
- PDF 页码：需人工复核
- 本地 PDF：{PDF}
- 处理状态：已精修 / 需人工复核

## 核心概念

{concept}

## 关键公式

- {formula}
- 公式符号、归一化系数和边界处理需对照原书人工复核。

## 算法步骤

1. 输入灰度图像或一维灰度序列。
2. 选择傅里叶或小波变换。
3. 将图像映射到频率/尺度系数域。
4. 可视化、筛选、增强、阈值化或压缩系数。
5. 需要图像结果时执行逆变换或归一化显示。

## 直观理解

变换不是改变图像本身，而是换一个角度观察图像：傅里叶看全局频率，小波看不同尺度和位置上的细节。

## 使用场景

频域滤波、周期噪声分析、图像压缩、融合、增强、小波去噪和多尺度特征提取。

## 优点

- 能解释空间域难以直接观察的频率或尺度结构。
- 便于针对不同频带或子带做处理。

## 局限性

- 变换系数不如像素直观。
- 边界、归一化和阈值选择会影响结果。

## 和相关方法的对比

- {compare}

## 教学图示

![{title}](../../assets/extracted_figures/{figure})

## 对应代码

{code_line}

## 相关知识

- [[04_图像去噪/4.5_非局部均值滤波|非局部均值滤波]]
- [[05_图像锐化/5.3_二阶微分算子|二阶微分算子]]
- [[10_图像压缩编码|图像压缩编码]]

## 复习问题

1. 本节方法把图像映射到了什么表示域？
2. 低频、高频或小波子带分别对应什么图像结构？
3. 参数或阈值选错会产生什么影响？
"""


def refine_wiki() -> None:
    WIKI.mkdir(parents=True, exist_ok=True)
    for item in FILES:
        (WIKI / item[0]).write_text(render(item), encoding="utf-8")
    (WIKI / "README.md").write_text("# 第 9 章 图像变换\n\n本章已升级为精品样板章节，覆盖傅里叶变换、FFT、频谱显示、小波分解和小波应用。\n", encoding="utf-8")


def add_semantic_edges() -> None:
    path = ROOT / "graph" / "semantic_edges.json"
    data = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {"nodes": [], "edges": []}
    nodes = {node["id"]: node for node in data.get("nodes", [])}
    edges = {(edge["source"], edge["target"], edge["type"]) for edge in data.get("edges", [])}
    def node(i: str, label: str, kind: str = "concept") -> None:
        nodes[i] = {"id": i, "label": label, "kind": kind}
    def edge(s: str, t: str, r: str) -> None:
        edges.add((s, t, r))
    for file, title, *_ in FILES:
        node(f"wiki/09_图像变换/{file}", title)
    for code in ["one_dimensional_fourier_transform.py", "two_dimensional_fft.py", "spectrum_visualization.py", "wavelet_decomposition.py", "wavelet_denoising.py"]:
        node(f"examples/09_image_transform/{code}", code, "code")
    for formula in ["DFT 公式", "FFT 复杂度", "频谱幅值", "小波多尺度分解", "小波阈值去噪"]:
        node(f"formula/ch09/{formula}", formula, "formula")
    edge("wiki/09_图像变换/9.1.3_快速傅里叶变换（FFT）.md", "wiki/09_图像变换/9.1_图像的频域变换（傅里叶变换）.md", "IMPROVES_OR_EXTENDS")
    edge("wiki/09_图像变换/9.2_小波变换.md", "wiki/09_图像变换/9.1_图像的频域变换（傅里叶变换）.md", "COMPARES_WITH")
    edge("wiki/09_图像变换/9.3_小波变换在图像处理中的应用.md", "wiki/09_图像变换/9.2_小波变换.md", "PREREQUISITE")
    for wiki, formula in [("9.1_图像的频域变换（傅里叶变换）.md", "DFT 公式"), ("9.1.3_快速傅里叶变换（FFT）.md", "FFT 复杂度"), ("9.1.4_图像的频谱分布特性.md", "频谱幅值"), ("9.2.3_小波的多尺度分解与重构.md", "小波多尺度分解"), ("9.3.4_应用于图像去噪.md", "小波阈值去噪")]:
        edge(f"wiki/09_图像变换/{wiki}", f"formula/ch09/{formula}", "USES_FORMULA")
    for wiki, code in [("9.1.1_一维傅里叶变换.md", "one_dimensional_fourier_transform.py"), ("9.1.2_二维傅里叶变换.md", "two_dimensional_fft.py"), ("9.1.4_图像的频谱分布特性.md", "spectrum_visualization.py"), ("9.2.3_小波的多尺度分解与重构.md", "wavelet_decomposition.py"), ("9.3.4_应用于图像去噪.md", "wavelet_denoising.py")]:
        edge(f"wiki/09_图像变换/{wiki}", f"examples/09_image_transform/{code}", "IMPLEMENTED_BY")
    edge("wiki/09_图像变换/9.3.1_应用于图像压缩.md", "wiki/10_图像压缩编码", "APPLIES_TO")
    data = {"nodes": sorted(nodes.values(), key=lambda x: x["id"]), "edges": [{"source": s, "target": t, "type": r} for s, t, r in sorted(edges)]}
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def update_docs() -> None:
    readme = ROOT / "README.md"
    text = readme.read_text(encoding="utf-8")
    text = text.replace("- 第 9 章到第 11 章仍在同一分支继续精修，当前不拆分独立分支，避免后续配置分散。", "- 第 9 章“图像变换”已升级为精品样板，包含原创图示、独立代码示例和语义图谱关系。\n- 第 10 章到第 11 章仍在同一分支继续精修，当前不拆分独立分支，避免后续配置分散。")
    if "第 9 章图像变换示例：" not in text:
        marker = "默认输入为 `assets/sample_images/` 中的合成图片，输出写入 `examples/output/`，该目录已被 `.gitignore` 忽略。"
        block = """第 9 章图像变换示例：

```powershell
python examples/09_image_transform/one_dimensional_fourier_transform.py
python examples/09_image_transform/two_dimensional_fft.py
python examples/09_image_transform/spectrum_visualization.py --gamma 0.4
python examples/09_image_transform/wavelet_decomposition.py --wavelet haar
python examples/09_image_transform/wavelet_denoising.py --threshold 12
```

"""
        text = text.replace(marker, block + marker)
    readme.write_text(text, encoding="utf-8")
    coverage = ROOT / "coverage_report.md"
    ctext = coverage.read_text(encoding="utf-8")
    ctext = ctext.replace("- 第 9 章到第 11 章：仍在同一分支继续精修，后续按第 2/3/4/5/6/7/8 章样板逐章推进。", "- 第 9 章：已精修为第八个精品样板，新增原创变换图示、独立可运行示例和语义图谱关系。\n- 第 10 章到第 11 章：仍在同一分支继续精修，后续按第 2/3/4/5/6/7/8/9 章样板逐章推进。")
    if "## 第 9 章处理记录" not in ctext:
        ctext += "\n\n## 第 9 章处理记录\n\n- 处理的 wiki 文件：第 9 章全部 15 个小节。\n- 新增原创教学图示：`ch09_fft_spectrum.png`、`ch09_frequency_filtering.png`、`ch09_wavelet_multiscale.png`、`ch09_wavelet_applications.png`。\n- 优化代码：`one_dimensional_fourier_transform.py`、`two_dimensional_fft.py`、`spectrum_visualization.py`、`wavelet_decomposition.py`、`wavelet_denoising.py`，并新增第 9 章 `_utils.py`。\n- 新增图谱关系：FFT 对傅里叶的 `IMPROVES_OR_EXTENDS`，傅里叶与小波的 `COMPARES_WITH`，小波应用的 `PREREQUISITE`，公式依赖和代码实现关系。\n- 仍需人工复核：原书页码、傅里叶归一化系数、小波基符号和边界延拓方式。\n- 未完成内容：未加入原书截图和原始文本；后续可加入更多滤波器设计和重构误差指标。\n"
    coverage.write_text(ctext, encoding="utf-8")
    (EX / "README.md").write_text("# 第 9 章 图像变换代码示例\n\n这些脚本默认使用 `assets/sample_images/sample_gray.png`，输出写入 `examples/output/`。\n", encoding="utf-8")


def main() -> None:
    refine_wiki()
    add_semantic_edges()
    update_docs()
    print("Refined chapter 9 image transform content.")


if __name__ == "__main__":
    main()
