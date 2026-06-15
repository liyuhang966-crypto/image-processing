"""Refine chapter notes into a consistent public knowledge-base structure."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WIKI = ROOT / "wiki"


CH02_EXAMPLES = {
    "2.1": "examples/02_image_enhancement/gamma_correction.py",
    "2.2": "examples/02_image_enhancement/contrast_stretching.py",
    "2.3": "examples/02_image_enhancement/gray_level_window.py",
    "2.3.1": "examples/02_image_enhancement/gray_level_window.py",
    "2.3.2": "examples/02_image_enhancement/gray_level_window.py",
    "2.4": "examples/02_image_enhancement/contrast_stretching.py",
    "2.4.1": "examples/02_image_enhancement/contrast_stretching.py",
    "2.4.2": "examples/02_image_enhancement/gamma_correction.py",
    "2.5": "examples/02_image_enhancement/histogram_equalization.py",
    "2.6": "examples/02_image_enhancement/adaptive_histogram_equalization.py",
    "2.7": "examples/02_image_enhancement/pseudo_color.py",
    "2.8": "examples/02_image_enhancement/retinex_enhancement.py",
}


CH02_FIGURES = {
    "2.1": "assets/extracted_figures/ch02_gamma_curves.png",
    "2.2": "assets/extracted_figures/ch02_contrast_stretching.png",
    "2.3": "assets/extracted_figures/ch02_gray_window_slicing.png",
    "2.3.1": "assets/extracted_figures/ch02_gray_window_slicing.png",
    "2.3.2": "assets/extracted_figures/ch02_gray_window_slicing.png",
    "2.5": "assets/extracted_figures/ch02_histogram_equalization.png",
    "2.6": "assets/extracted_figures/ch02_adaptive_histogram_equalization.png",
    "2.7": "assets/extracted_figures/ch02_pseudo_color_lut.png",
    "2.8": "assets/extracted_figures/ch02_retinex_decomposition.png",
}


CH02_PROFILES = {
    "2.1": {
        "concept": "γ校正用幂律映射重新分配灰度。它不改变像素位置，只改变亮度响应曲线，常用于校正显示设备、相机响应或让暗部/亮部细节更容易观察。",
        "formula": r"s = c r^{\gamma},\quad r,s\in[0,1]",
        "steps": ["把输入灰度归一化到 0 到 1。", "选择 γ：小于 1 提亮暗部，大于 1 压暗亮部。", "逐像素执行幂律映射。", "重新量化到 8 位或目标位深，并检查是否出现饱和。"],
        "intuition": "把灰度轴当作橡皮筋：γ<1 会拉开暗部、压缩亮部；γ>1 则相反。",
        "scene": "显示校正、医学图像暗部观察、曝光不足图像的初步增强。",
        "pros": "实现简单、参数直观、计算量低。",
        "limits": "全局参数无法适应局部照明变化；γ 选得过激会丢失亮部或暗部层次。",
        "compare": "相较直方图均衡化，γ校正更可控但不会自动均衡灰度分布；相较 Retinex，它不显式分离照明和反射。",
        "review": ["为什么处理前通常先归一化灰度？", "γ<1 和 γ>1 分别适合什么图像？", "γ校正和线性展宽的灰度映射曲线有什么差异？"],
    },
    "2.2": {
        "concept": "对比度线性展宽通过分段线性函数把输入灰度区间拉伸到更大的输出区间，使目标灰度范围占用更多显示动态范围。",
        "formula": r"s=\begin{cases}0,&r\le a\\ \frac{r-a}{b-a}(L-1),&a<r<b\\ L-1,&r\ge b\end{cases}",
        "steps": ["估计有效灰度下限 a 和上限 b。", "建立分段线性映射，低于 a 的值压到黑，高于 b 的值压到白。", "对所有像素映射并裁剪到合法范围。", "用直方图确认有效灰度是否被拉开。"],
        "intuition": "像把挤在中间的一段灰度拉满整个显示标尺。",
        "scene": "低对比度扫描件、雾化图像、灰度范围窄但噪声不严重的图像。",
        "pros": "可解释、可控、速度快，适合做增强流水线的基线。",
        "limits": "端点选择敏感；若噪声处在端点附近，噪声也会被放大。",
        "compare": "比动态范围自动拉伸更依赖人工端点；比直方图均衡化更保留原有灰度次序和整体观感。",
        "review": ["端点 a、b 选得太靠内会发生什么？", "线性展宽为什么可能放大噪声？", "它和灰级窗的目标区域有什么不同？"],
    },
    "2.3": {
        "concept": "灰级窗和灰级窗切片都围绕某个灰度区间工作：前者强调窗口内细节，后者把窗口内像素作为目标区域突出显示。",
        "formula": r"W=[a,b],\quad s=f(r\mid r\in W)",
        "steps": ["确定感兴趣灰度窗口 W。", "决定窗口内是线性显示、增强显示还是二值突出。", "决定窗口外保留、压低还是置零。", "检查目标是否被突出且背景是否仍可判读。"],
        "intuition": "灰级窗像调手电筒照亮某段灰度；切片像给这段灰度贴醒目标记。",
        "scene": "医学窗宽窗位观察、材料缺陷检测、遥感特定地物增强。",
        "pros": "能把注意力集中到指定灰度范围。",
        "limits": "灰度范围和目标语义不是一一对应时容易误检。",
        "compare": "比全局增强更聚焦；比阈值分割保留更多灰度上下文。",
        "review": ["灰级窗和灰级窗切片的输出形式有什么区别？", "窗口外像素保留或置零分别适合什么任务？", "为什么灰度相同不一定代表同一物体？"],
    },
    "2.3.1": {
        "concept": "灰级窗是在指定灰度范围内进行细节观察的窗口化显示方法，常由窗宽和窗位描述。",
        "formula": r"center=\frac{a+b}{2},\quad width=b-a",
        "steps": ["确定窗位中心和窗宽。", "把窗口内灰度映射到可见范围。", "对窗口外灰度执行饱和或压缩。", "根据视觉目标迭代调整窗宽窗位。"],
        "intuition": "窗宽越窄，局部对比越强但可见范围越小。",
        "scene": "CT/MRI 灰度观察、工业无损检测的局部灰度检查。",
        "pros": "对特定灰度组织或材料非常直观。",
        "limits": "不同窗口之间的信息不能一次性全部呈现。",
        "compare": "与γ校正相比，灰级窗强调区间选择；与线性展宽相比，它通常接受窗口外饱和。",
        "review": ["窗宽变窄会带来什么视觉变化？", "窗位移动对应观察哪类灰度？", "为什么一个图像可能需要多个窗位？"],
    },
    "2.3.2": {
        "concept": "灰级窗切片把某个灰度区间视为目标切片，通常把窗口内像素提升到高亮或指定颜色，以突出目标。",
        "formula": r"s=\begin{cases}L-1,&a\le r\le b\\ r\text{ 或 }0,&otherwise\end{cases}",
        "steps": ["选定切片灰度区间。", "设置窗口内输出值或伪彩色。", "选择窗口外保留原灰度还是压低背景。", "统计命中区域，必要时和形态学或连通域分析结合。"],
        "intuition": "它像在灰度轴上切下一片，把这片对应的像素在图上点亮。",
        "scene": "目标灰度已知的缺陷提取、遥感水体/植被粗定位、医学病灶候选区域提示。",
        "pros": "目标突出强，后续分割容易接入。",
        "limits": "对照明变化和同灰度干扰敏感。",
        "compare": "比阈值分割多了保留背景的选择；比伪彩色更偏检测而非显示美化。",
        "review": ["切片窗口外保留原值有什么好处？", "为什么灰级窗切片不等同于最终分割？", "它和伪彩色 LUT 如何结合？"],
    },
    "2.4": {
        "concept": "动态范围调整改变图像可表示灰度范围的占用方式，目标是在显示、存储或后续算法前改善有效层次。",
        "formula": r"s=T(r),\quad T \text{ 可为线性或非线性映射}",
        "steps": ["分析当前最小/最大灰度和主要灰度分布。", "确定线性、分段线性或非线性映射。", "执行映射并裁剪。", "用视觉结果和直方图共同判断。"],
        "intuition": "动态范围调整是在重新分配有限的灰度预算。",
        "scene": "位深转换、显示预处理、增强算法前的灰度标准化。",
        "pros": "概念统一，可覆盖多类增强映射。",
        "limits": "只改强度不理解图像内容，不能单独解决模糊或噪声。",
        "compare": "线性方法强调比例保持；非线性方法强调按视觉或任务需求重新分配。",
        "review": ["动态范围和对比度有什么联系？", "什么时候线性调整已经足够？", "非线性调整为什么可能更符合视觉感受？"],
    },
    "2.4.1": {
        "concept": "线性动态范围调整用一次函数或分段一次函数把输入区间映射到输出区间，保持灰度顺序和相对比例。",
        "formula": r"s=\frac{r-r_{min}}{r_{max}-r_{min}}(s_{max}-s_{min})+s_{min}",
        "steps": ["统计输入有效范围。", "指定目标输出范围。", "按线性公式映射。", "处理越界值和空范围异常。"],
        "intuition": "像把一把短尺按比例拉成一把长尺。",
        "scene": "低动态范围图像显示、传感器输出归一化、算法输入标准化。",
        "pros": "灰度关系稳定，便于解释和复现。",
        "limits": "不能针对局部区域单独增强。",
        "compare": "比γ校正更直；比直方图均衡化更少改变灰度统计结构。",
        "review": ["为什么需要处理 r_max=r_min 的异常？", "线性映射是否会改变像素排序？", "线性调整和归一化有什么关系？"],
    },
    "2.4.2": {
        "concept": "非线性动态范围调整用对数、指数、幂律等曲线，对不同灰度段给出不同增强力度。",
        "formula": r"s=c\log(1+r)\quad\text{或}\quad s=c r^\gamma",
        "steps": ["判断需要突出暗部、亮部还是压缩高动态范围。", "选择对数、指数或幂律函数。", "归一化输入并执行映射。", "结合直方图和视觉结果调整参数。"],
        "intuition": "非线性映射像弯曲灰度尺，让某些区间拥有更多刻度。",
        "scene": "暗部细节增强、频谱图显示、强光区域动态压缩。",
        "pros": "能更贴合人眼或任务对不同亮度段的关注。",
        "limits": "参数不当会造成层次挤压或灰度断裂。",
        "compare": "比线性调整灵活；比 Retinex 简单但不处理空间照明估计。",
        "review": ["对数变换为什么常用于压缩大范围数值？", "非线性调整为何容易产生过增强？", "如何用直方图辅助调参？"],
    },
    "2.5": {
        "concept": "直方图均衡化利用累计分布函数重新映射灰度，使输出灰度分布更接近均匀，从而提高整体对比度。",
        "formula": r"s_k=(L-1)\sum_{j=0}^{k}p_r(r_j)",
        "steps": ["统计灰度直方图。", "归一化得到概率分布。", "计算累计分布函数 CDF。", "用 CDF 建立查找表并映射所有像素。"],
        "intuition": "把出现过密的灰度段摊开，把过稀的灰度段合并。",
        "scene": "整体偏暗/偏亮且灰度集中图像的快速增强。",
        "pros": "自动化程度高，不需要手动选择端点。",
        "limits": "可能放大噪声，局部区域可能过增强，亮度风格可能变化明显。",
        "compare": "比线性展宽更自适应；比 CLAHE 更全局，无法限制局部噪声放大。",
        "review": ["CDF 为什么能作为灰度映射函数？", "均衡化后直方图一定完全平坦吗？", "什么时候直方图均衡化不适合直接使用？"],
    },
    "2.6": {
        "concept": "自适应直方图均衡化在局部窗口内执行均衡化，CLAHE 进一步用裁剪限制避免噪声被过度放大。",
        "formula": r"s(x,y)=T_{\Omega(x,y)}(r(x,y))",
        "steps": ["把图像划分为网格或局部窗口。", "在每个局部区域统计直方图。", "必要时裁剪直方图峰值并重新分配。", "插值融合相邻区域映射结果，避免块效应。"],
        "intuition": "不是给整张图一套增强规则，而是给每块区域一套更贴近局部的规则。",
        "scene": "医学图像、低照度图像、局部对比不足的纹理观察。",
        "pros": "局部细节增强明显，可配合裁剪限制噪声。",
        "limits": "参数更多，计算量更大；窗口过小会产生块感或增强噪声。",
        "compare": "比全局均衡更重视局部；比 Retinex 更偏统计映射，不显式建模光照。",
        "review": ["CLAHE 中 clipLimit 的作用是什么？", "窗口大小如何影响增强效果？", "为什么需要区域间插值？"],
    },
    "2.7": {
        "concept": "伪彩色把单通道灰度映射为彩色，以利用人眼对颜色差异的敏感性突出灰度层次。",
        "formula": r"(R,G,B)=LUT(r)",
        "steps": ["选择色表或设计灰度到颜色的 LUT。", "把每个灰度值映射为 RGB。", "检查色表是否符合数值含义，避免误导。", "必要时保留颜色条解释映射。"],
        "intuition": "它不增加原始信息，而是把灰度差异换成人眼更容易分辨的颜色差异。",
        "scene": "热力图、遥感单波段显示、医学或工业强度场可视化。",
        "pros": "显示直观，能突出细微灰度层次。",
        "limits": "色表选择可能制造虚假边界或误读强弱关系。",
        "compare": "不同于彩色图像处理，伪彩色输入通常仍是灰度；不同于灰级窗切片，它可连续映射全灰度范围。",
        "review": ["伪彩色是否增加图像信息？", "为什么需要配色条？", "连续色表和分段色表适用场景有何不同？"],
    },
    "2.8": {
        "concept": "Retinex 将图像理解为照明与反射的组合，通过估计并削弱照明分量来增强反射细节和颜色恒常性。",
        "formula": r"R(x,y)=\log I(x,y)-\log(F(x,y)*I(x,y))",
        "steps": ["把输入转为浮点并避免零值。", "用高斯核等方法估计照明分量。", "在对数域相减得到反射近似。", "归一化或颜色恢复后输出增强图像。"],
        "intuition": "Retinex 试图区分“物体本来的反射特性”和“照在它上面的光”。",
        "scene": "不均匀照明、逆光、低照度、颜色恒常性增强。",
        "pros": "对局部照明变化更有针对性，能同时改善亮度和颜色观感。",
        "limits": "尺度和参数敏感，可能产生光晕、颜色偏移或噪声增强。",
        "compare": "比γ校正、直方图均衡化更接近光照模型；比深度学习方法轻量但表达能力有限。",
        "review": ["Retinex 为什么常在对数域计算？", "高斯尺度大小会影响什么？", "它和 CLAHE 都能增强局部细节，核心差别是什么？"],
    },
}


CHAPTER_PROFILES = {
    "03": ("图像几何变换", "坐标映射、插值和几何校正", "把像素从一个坐标系重采样到另一个坐标系，核心是变换矩阵和插值策略。", "examples/03_geometric_transform"),
    "04": ("图像去噪", "噪声模型、邻域滤波和结构保持", "在降低随机扰动的同时尽量保留边缘、纹理和细小目标。", "examples/04_image_denoising"),
    "05": ("图像锐化", "微分算子、边缘和细节增强", "用梯度或二阶导数突出灰度突变，服务于视觉增强和边缘检测。", "examples/05_image_sharpening"),
    "06": ("图像的分割", "阈值、区域和目标提取", "把像素组织成有意义的区域，是从图像增强走向图像理解的关键步骤。", "examples/06_image_segmentation"),
    "07": ("二值图像处理", "连通性、形态学和标签", "在二值集合上操作目标形状、拓扑关系和连通区域。", "examples/07_binary_image_processing"),
    "08": ("彩色图像处理", "颜色模型、白平衡和颜色校正", "把颜色从物理光谱、视觉感知和计算表示三个层面联系起来。", "examples/08_color_image_processing"),
    "09": ("图像变换", "频域、小波和多尺度表示", "把图像换到更适合分析、压缩或滤波的表示域。", "examples/09_image_transform"),
    "10": ("图像压缩编码", "冗余、无损和有损编码", "用统计冗余、视觉冗余和变换稀疏性降低存储与传输成本。", "examples/10_image_compression"),
    "11": ("深度学习与图像处理", "卷积网络、超分辨率、分类和检测", "用可学习的多层特征替代手工规则，解决复原、识别和检测任务。", "examples/11_deep_learning_image_processing"),
}


GENERIC_FORMULAS = {
    "03": r"\begin{bmatrix}x'\\y'\\1\end{bmatrix}=H\begin{bmatrix}x\\y\\1\end{bmatrix}",
    "04": r"g(x,y)=\sum_{(i,j)\in\Omega}w(i,j)f(x-i,y-j)",
    "05": r"|\nabla f|=\sqrt{G_x^2+G_y^2},\quad \nabla^2 f=f_{xx}+f_{yy}",
    "06": r"g(x,y)=\begin{cases}1,&f(x,y)\ge T\\0,&f(x,y)<T\end{cases}",
    "07": r"A\oplus B=\{z\mid(\hat{B})_z\cap A\ne\varnothing\},\quad A\ominus B=\{z\mid B_z\subseteq A\}",
    "08": r"\begin{bmatrix}R\\G\\B\end{bmatrix}\leftrightarrow \begin{bmatrix}Y\\Cb\\Cr\end{bmatrix}\ \text{或}\ \begin{bmatrix}H\\S\\V\end{bmatrix}",
    "09": r"F(u,v)=\sum_x\sum_y f(x,y)e^{-j2\pi(ux/M+vy/N)}",
    "10": r"R=\frac{\text{原始数据量}}{\text{编码后数据量}},\quad H=-\sum_i p_i\log_2 p_i",
    "11": r"y_k=\sigma\left(\sum_c W_{k,c}*x_c+b_k\right)",
}


def extract_prefix(path: Path) -> str:
    return path.stem.split("_", 1)[0]


def title_from_path(path: Path) -> str:
    return path.stem if path.stem != "README" else path.parent.name


def preserve_reading_block(text: str) -> str:
    if text.startswith("> [!note]"):
        marker = "\n## 来源\n"
        if marker in text:
            return text.split(marker, 1)[0].rstrip() + "\n\n"
    return ""


def relative_link(path: Path, target: str) -> str:
    return Path(target).as_posix()


def related_links_for_ch02(prefix: str) -> list[str]:
    order = ["2.1", "2.2", "2.3", "2.3.1", "2.3.2", "2.4", "2.4.1", "2.4.2", "2.5", "2.6", "2.7", "2.8"]
    labels = {
        "2.1": "2.1_γ校正",
        "2.2": "2.2_对比度线性展宽",
        "2.3": "2.3_灰级窗与灰级窗切片",
        "2.3.1": "2.3.1_灰级窗",
        "2.3.2": "2.3.2_灰级窗切片",
        "2.4": "2.4_动态范围调整",
        "2.4.1": "2.4.1_线性动态范围调整",
        "2.4.2": "2.4.2_非线性动态范围调整",
        "2.5": "2.5_直方图均衡化",
        "2.6": "2.6_自适应直方图均衡化",
        "2.7": "2.7_伪彩色",
        "2.8": "2.8_Retinex图像增强方法",
    }
    if prefix not in order:
        return ["[[2.1_γ校正]]", "[[2.5_直方图均衡化]]", "[[2.8_Retinex图像增强方法]]"]
    idx = order.index(prefix)
    candidates = order[max(0, idx - 2):idx] + order[idx + 1:idx + 3]
    return [f"[[{labels[item]}]]" for item in candidates]


def write_ch02_note(path: Path) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    prefix = extract_prefix(path)
    title = title_from_path(path)
    if prefix == "2.x":
        body = f"""# {title}

{preserve_reading_block(old)}## 复习定位

本页用于把第 2 章的增强方法串成可复习的问题链。重点不是背答案，而是能判断一张图应该先用哪类增强、为什么、以及增强后可能引入什么副作用。

## 问题清单

1. 给定一张整体偏暗图像，如何在 γ校正、线性展宽、直方图均衡化之间选择？
2. 灰级窗、灰级窗切片和阈值分割分别强调什么输出目标？
3. 全局直方图均衡化为什么可能放大噪声？CLAHE 怎样缓解？
4. 伪彩色改变的是信息量还是显示方式？如何避免色表误导？
5. Retinex 的照明-反射分解思想与普通灰度映射有什么差别？

## 关系索引

- [[2.1_γ校正]]
- [[2.2_对比度线性展宽]]
- [[2.3_灰级窗与灰级窗切片]]
- [[2.5_直方图均衡化]]
- [[2.6_自适应直方图均衡化]]
- [[2.8_Retinex图像增强方法]]
"""
        path.write_text(body, encoding="utf-8")
        return

    profile = CH02_PROFILES[prefix]
    figure = CH02_FIGURES.get(prefix)
    figure_block = ""
    if figure:
        figure_block = f"\n## 教学图示\n\n![{title} 教学图示](../../{figure})\n\n该图为本仓库生成的原创教学示意图，不是原书截图；用于公开仓库展示和复习。\n"
    example = CH02_EXAMPLES.get(prefix, "examples/02_image_enhancement/README.md")
    related = "\n".join(f"- {link}" for link in related_links_for_ch02(prefix))
    steps = "\n".join(f"{i}. {step}" for i, step in enumerate(profile["steps"], 1))
    reviews = "\n".join(f"{i}. {item}" for i, item in enumerate(profile["review"], 1))
    content = f"""# {title}

{preserve_reading_block(old)}## 核心概念

{profile["concept"]}

## 关键公式

```math
{profile["formula"]}
```

公式中的符号按通用数字图像处理记号整理；与原书具体编号、边界取值或变量命名不一致处，后续逐页核对时标注“需人工复核”。

## 算法步骤

{steps}

## 直观理解

{profile["intuition"]}

## 使用场景

{profile["scene"]}

## 优点

{profile["pros"]}

## 局限性

{profile["limits"]}

## 和其他增强方法的对比

{profile["compare"]}
{figure_block}
## 对应代码

- [{example}](../../{example})

## 相关知识

{related}

## 复习问题

{reviews}
"""
    path.write_text(content, encoding="utf-8")


def write_later_note(path: Path, chapter: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    title = title_from_path(path)
    chapter_title, keywords, concept, examples = CHAPTER_PROFILES[chapter]
    chapter_link = path.parent.name
    formula = GENERIC_FORMULAS[chapter]
    prefix = extract_prefix(path)
    if prefix.endswith(".x"):
        content = f"""# {title}

{preserve_reading_block(old)}## 复习定位

本页先把第 {int(chapter)} 章习题整理成知识检查清单。题目细节仍需对照合法本地 PDF 人工核对，本仓库不公开原书 PDF 或逐题原文。

## 复习问题

1. 本章最核心的输入、输出和中间表示分别是什么？
2. 本章方法依赖哪些前置章节？会为哪些后续章节提供基础？
3. 常用公式中的变量含义、边界条件和适用假设是什么？
4. 如果用代码验证，本章最小可运行示例应覆盖哪一种典型输入？
5. 哪些失败案例最容易暴露参数选择或任务假设问题？

## 相关知识

- [[{chapter_link}|{chapter_title}]]
- [[00_导航]]
- [[99_术语表]]
"""
        path.write_text(content, encoding="utf-8")
        return

    content = f"""# {title}

{preserve_reading_block(old)}## 精修状态

本页已从占位笔记升级为结构化精修初版，覆盖核心概念、公式、步骤、场景和复习问题；图示、页码和书中符号仍需后续逐页人工复核。

## 核心概念

{concept} 当前小节聚焦“{title}”，应放在第 {int(chapter)} 章“{chapter_title}”的整体链路中理解，关键词是：{keywords}。

## 关键公式

```math
{formula}
```

上式是本章常用表达的复习锚点，不代表原书中本小节唯一公式；具体编号、符号和推导细节需人工复核。

## 算法步骤

1. 明确输入图像、参数和目标输出。
2. 根据本节方法建立局部或全局处理规则。
3. 对像素、邻域、区域、频域系数或特征图执行对应变换。
4. 检查边界条件、数值范围和可视化结果。
5. 将结果与本章其他方法比较，判断是否满足任务目标。

## 直观理解

把本节看作处理流水线中的一个可替换模块：它改变的是坐标、灰度、噪声、边缘、区域、颜色、频域表示、编码长度或语义特征中的某一类信息。

## 使用场景

适合用于课程复习、实验代码定位、算法选型前的概念判断，以及和前后章节建立知识图谱关系。

## 优点

- 结构清楚，便于和代码示例、图谱节点互相跳转。
- 保留了方法的输入输出和适用条件，减少只背名称造成的混淆。

## 局限性

- 尚未逐页补齐原书图示和所有公式。
- 参数、边界处理和实验结论仍需结合本地合法 PDF 与代码运行结果复核。

## 和相关方法的对比

本节应与本章相邻小节对比：看它是全局还是局部、线性还是非线性、确定性规则还是数据驱动、增强显示还是提取结构。必要时继续连接到第 2 章增强、第 4 章去噪、第 6 章分割或第 11 章深度学习方法。

## 对应代码

- [{examples}/README.md](../../{examples}/README.md)

## 相关知识

- [[{chapter_link}|{chapter_title}]]
- [[00_导航]]
- [[99_术语表]]

## 复习问题

1. 本节处理对象是什么：像素灰度、空间坐标、邻域结构、频域系数还是语义特征？
2. 本节最关键的参数是什么？参数过大或过小会产生什么现象？
3. 本节与本章前一个方法相比，解决了什么问题，又引入了什么限制？
4. 如何设计一个最小合成图像来验证本节方法？
"""
    path.write_text(content, encoding="utf-8")


def write_chapter_readme(path: Path, chapter: str) -> None:
    chapter_title, keywords, concept, examples = CHAPTER_PROFILES[chapter]
    notes = sorted(p for p in path.parent.glob("*.md") if p.name != "README.md")
    links = "\n".join(f"- [[{note.stem}]]" for note in notes)
    content = f"""# {chapter_title}

## 章节定位

{concept}

## 本章关键词

{keywords}

## 精修状态

本章已从空壳占位升级为结构化精修初版。当前版本适合复习和知识图谱浏览；公式编号、原书图示和个别术语仍需后续对照本地合法 PDF 人工复核。

## 小节索引

{links}

## 代码入口

- [{examples}/README.md](../../{examples}/README.md)
"""
    path.write_text(content, encoding="utf-8")


def update_project_docs() -> None:
    readme = """# 数字图像处理知识库

这是一个由 Codex 长期维护的 Obsidian 风格个人学习知识库，围绕《数字图像处理基础（朱虹）》进行转述、归纳和实验化整理。

## 当前进度

- 全书目录已初步覆盖，`wiki/` 中已经建立第 1 章到第 11 章的章节与小节入口。
- 第 1 章已完成基础细化，可作为概念入口。
- 第 2 章已进入重点精修，并补充公式、算法步骤、原创教学图示、代码链接和复习问题。
- 第 3 章到第 11 章已按同一模板升级为结构化精修初版，后续仍需逐章补图、复核公式和深化例题。
- `raw/books/`、`raw/extracted_text/` 和 `raw/temp/` 只用于本地处理，不应提交公开仓库；公开仓库不包含原书 PDF 或原始抽取文本。

## 本地 PDF 阅读

公开仓库不显示原书 PDF。若你拥有合法副本，可在本地放入：

```text
raw/books/数字图像处理基础_朱虹.pdf
```

每个 wiki 小节顶部的 Obsidian 内嵌 PDF 阅读块会从对应页码打开，便于边看整理笔记边核对原书。

## 入口

- `index.md`
- `wiki/00_导航.md`
- `wiki/99_术语表.md`
- `graph/knowledge_graph.json`
- `graph/mermaid_graph.md`
- `graph/knowledge_graph.html`
- `coverage_report.md`

## 校验

```powershell
python -m unittest discover -s tests
python tools/check_links.py
python tools/health_check.py
```
"""
    (ROOT / "README.md").write_text(readme, encoding="utf-8")

    agents = """# Codex 维护规则

本项目是《数字图像处理基础（朱虹）》的个人学习知识库。`wiki/` 是整理后的知识库主体，由 Codex 维护。

## 资料和空间

- 原始 PDF 在 `C:\\Users\\lizi\\Desktop\\学习\\数字图像处理基础 (朱虹)(1).pdf`，不要移动。
- 项目内处理路径是 `raw/books/数字图像处理基础_朱虹.pdf`，`raw/books/*` 默认不提交。
- `raw/extracted_text/*` 与 `raw/temp/*` 只用于本地处理，公开仓库只保留 README 占位文件。
- 优先节省本地空间：不要批量导出全书图片；只生成或提取 wiki 真正引用的教学图。

## 内容规则

- 不要大段复制原书全文；wiki 只能整理、转述、归纳。
- 不确定的公式、页码、图片、表格，必须标注“需人工复核”。
- 公开仓库不上传原书 PDF、原始抽取文本或原书截图；可提交原创教学示意图和合成样例。
- 修改 wiki 时，同步检查 `index.md`、`wiki/00_导航.md`、`wiki/99_术语表.md`、`graph/knowledge_graph.json`、`graph/mermaid_graph.md`、`coverage_report.md`。
- 不要下载模型、数据集，不要调用外部 API。

## 当前重点

第 2 章作为精品样板继续维护；第 3 章到第 11 章已经结构化，后续逐章补图、复核公式、加深代码实验。
"""
    (ROOT / "AGENTS.md").write_text(agents, encoding="utf-8")

    index = """# 数字图像处理知识库索引

## 快速入口

- [[wiki/00_导航|导航]]
- [[wiki/99_术语表|术语表]]
- [[wiki/01_引言/README|第 1 章 引言]]
- [[wiki/02_图像增强/README|第 2 章 图像增强]]
- [知识图谱 JSON](graph/knowledge_graph.json)
- [Mermaid 知识图谱](graph/mermaid_graph.md)
- [HTML 知识图谱](graph/knowledge_graph.html)

## 维护状态

- 全书目录：已覆盖。
- 第 1 章：已细化。
- 第 2 章：重点精修样板。
- 第 3-11 章：结构化精修初版，待继续逐章补图和公式复核。

## 公开仓库边界

`raw/books/`、`raw/extracted_text/` 和 `raw/temp/` 不提交实际资料文件。若需在 Obsidian 中查看内嵌 PDF，请在本地放入合法副本。
"""
    (ROOT / "index.md").write_text(index, encoding="utf-8")

    nav = """# 导航

## 章节

- [[01_引言/README|第 1 章 引言]]
- [[02_图像增强/README|第 2 章 图像增强]]
- [[03_图像几何变换/README|第 3 章 图像几何变换]]
- [[04_图像去噪/README|第 4 章 图像去噪]]
- [[05_图像锐化/README|第 5 章 图像锐化]]
- [[06_图像的分割/README|第 6 章 图像的分割]]
- [[07_二值图像处理/README|第 7 章 二值图像处理]]
- [[08_彩色图像处理/README|第 8 章 彩色图像处理]]
- [[09_图像变换/README|第 9 章 图像变换]]
- [[10_图像压缩编码/README|第 10 章 图像压缩编码]]
- [[11_深度学习与图像处理/README|第 11 章 深度学习与图像处理]]

## 图谱与报告

- [Mermaid 知识图谱](../graph/mermaid_graph.md)
- [HTML 知识图谱](../graph/knowledge_graph.html)
- [覆盖报告](../coverage_report.md)
"""
    (WIKI / "00_导航.md").write_text(nav, encoding="utf-8")

    glossary = """# 术语表

## 图像增强

- γ校正：用幂律曲线调整亮度响应，常用于暗部或亮部层次调整。
- 线性展宽：把有效灰度区间线性映射到更宽输出范围。
- 灰级窗：围绕指定灰度区间进行窗口化显示。
- 灰级窗切片：突出指定灰度区间对应像素，可保留或压低背景。
- 直方图均衡化：用累计分布函数重新映射灰度，提高全局对比度。
- CLAHE：带对比度限制的局部直方图均衡化。
- 伪彩色：把灰度值映射到颜色表，增强可视化辨识度。
- Retinex：基于照明和反射分解的增强思想。

## 后续章节关键词

- 几何变换：平移、镜像、旋转、缩放、错切、仿射、畸变校正。
- 去噪：均值滤波、中值滤波、边界保持、非局部均值。
- 锐化：梯度、Laplacian、Sobel、Roberts、Prewitt、Canny、LOG。
- 分割：阈值、最大熵、类间方差、区域生长。
- 二值图像：连通性、腐蚀、膨胀、开运算、闭运算、标签、细线化。
- 彩色处理：RGB、HSV、YCbCr、白平衡、灰色世界、色彩补偿。
- 图像变换：傅里叶变换、FFT、小波变换、多尺度分解。
- 压缩编码：冗余、RLE、Huffman、有损编码、小波编码。
- 深度学习：卷积层、激活层、BN、池化、SRCNN、ESPCN、LeNet、AlexNet、Faster R-CNN、YOLO。
"""
    (WIKI / "99_术语表.md").write_text(glossary, encoding="utf-8")

    graph_readme = """# 知识图谱

`wiki/` 的 Obsidian 链接是当前知识图谱主数据源。运行：

```powershell
python tools/build_graph_from_wiki.py
```

会同步生成：

- `graph/knowledge_graph.json`
- `graph/mermaid_graph.md`
- `graph/knowledge_graph.html`

`data/raw/entities.csv` 和 `data/raw/relations.csv` 仅保留为 starter 示例，不再作为公开图谱的主来源。
"""
    (ROOT / "graph" / "README.md").write_text(graph_readme, encoding="utf-8")

    coverage = """# 覆盖检查报告

## 总体状态

- 全书目录：已初步覆盖。
- 第 1 章：已细化。
- 第 2 章：已精修为后续章节样板，包含核心概念、关键公式、算法步骤、直观理解、使用场景、优点、局限性、方法对比、代码链接和复习问题。
- 第 3 章到第 11 章：已升级为结构化精修初版，仍待逐章补图、复核公式和深化例题。

## 公开仓库边界

- `raw/books/*` 不提交，公开仓库不包含原书 PDF。
- `raw/extracted_text/*` 不提交，公开仓库不包含原始抽取文本。
- `raw/temp/*` 不提交。
- 上述目录仅保留 README 占位文件。

## 第 2 章教学图示

本次只生成第 2 章必要教学图示，保存于 `assets/extracted_figures/`：

- `ch02_gamma_curves.png`
- `ch02_contrast_stretching.png`
- `ch02_gray_window_slicing.png`
- `ch02_histogram_equalization.png`
- `ch02_adaptive_histogram_equalization.png`
- `ch02_pseudo_color_lut.png`
- `ch02_retinex_decomposition.png`

这些图是原创教学示意图，不是原书截图，可提交公开仓库。

## 公式复核

- 第 2 章常用公式已补入，但符号、页码和原书编号仍需人工复核。
- 第 3 章到第 11 章只放入章节级复习锚点公式，不宣称逐小节完整覆盖。

## 代码运行检查

第 2 章示例计划逐个检查：

- `gamma_correction.py`
- `contrast_stretching.py`
- `gray_level_window.py`
- `histogram_equalization.py`
- `adaptive_histogram_equalization.py`
- `pseudo_color.py`
- `retinex_enhancement.py`

验证命令见 README；实际运行结果以本次 PR 的终端检查为准。

## 图谱生成

- 主数据源：`wiki/` 的 Obsidian 链接。
- 输出：`graph/knowledge_graph.json`、`graph/mermaid_graph.md`、`graph/knowledge_graph.html`。
- `src/graph_builder.py` 默认调用 wiki 图谱生成逻辑；CSV 构建函数仅保留用于 starter 测试兼容。
"""
    (ROOT / "coverage_report.md").write_text(coverage, encoding="utf-8")


def main() -> None:
    for path in sorted((WIKI / "02_图像增强").glob("*.md")):
        if path.name == "README.md":
            path.write_text(
                "# 图像增强\n\n## 章节定位\n\n第 2 章是本知识库的重点精修样板，围绕灰度映射、直方图、伪彩色和 Retinex 等方法建立增强方法谱系。\n\n## 小节索引\n\n"
                + "\n".join(f"- [[{note.stem}]]" for note in sorted(path.parent.glob("*.md")) if note.name != "README.md")
                + "\n\n## 教学图示\n\n第 2 章原创教学图示位于 [assets/extracted_figures](../../assets/extracted_figures/README.md)。\n",
                encoding="utf-8",
            )
        else:
            write_ch02_note(path)

    for chapter in CHAPTER_PROFILES:
        folder = next(WIKI.glob(f"{chapter}_*"))
        for path in sorted(folder.glob("*.md")):
            if path.name == "README.md":
                write_chapter_readme(path, chapter)
            else:
                write_later_note(path, chapter)

    update_project_docs()
    print("Refined chapter 2 and structured chapters 3-11.")


if __name__ == "__main__":
    main()
