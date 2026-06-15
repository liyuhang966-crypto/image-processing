"""Refine chapter 4 image denoising notes and semantic graph overlay."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CH4 = ROOT / "wiki" / "04_图像去噪"
PDF_PATH = "raw/books/数字图像处理基础_朱虹.pdf"


PROFILES = {
    "4.1_图像噪声.md": {
        "section": "4.1 图像噪声",
        "book": "64",
        "pdf": "79",
        "figure": "ch04_noise_models.png",
        "code": "examples/04_image_denoising/README.md",
        "concept": "图像噪声是成像、传输或量化过程中叠加到真实图像上的随机扰动。理解噪声类型是选择去噪方法的前提：高斯噪声适合均值类平滑，椒盐噪声更适合中值滤波，纹理重复图像可考虑非局部均值。",
        "formula": r"g(x,y)=f(x,y)+n(x,y),\quad n\sim\mathcal{N}(0,\sigma^2)\quad\text{或}\quad P(g=0/255)>0",
        "steps": ["输入待分析图像。", "观察噪声形态：连续颗粒、孤立黑白点、条纹还是压缩伪影。", "估计噪声强度和是否与图像结构相关。", "选择候选滤波器并保留原图作为对照。", "用视觉结果和边缘/纹理保持情况评估。"],
        "intuition": "去噪不是把图像磨平，而是在猜哪些变化是随机干扰、哪些变化是真实边缘和纹理。",
        "scene": "低照度拍摄、扫描件清理、医学图像预处理、工业检测前的干扰抑制。",
        "pros": "先识别噪声模型能减少盲目调参。",
        "limits": "真实图像噪声往往混合存在，单一模型只能近似。",
        "compare": "高斯噪声常用均值或高斯滤波；椒盐噪声常用中值滤波；纹理重复场景适合非局部均值。",
        "links": ["[[4.2_均值滤波]]", "[[4.3_中值滤波]]", "[[4.5_非局部均值滤波]]", "[[2.5_直方图均衡化]]"],
        "review": ["高斯噪声和椒盐噪声在图像上各有什么表现？", "为什么去噪前要判断噪声类型？", "去噪为什么可能损伤边缘？"],
    },
    "4.2_均值滤波.md": {
        "section": "4.2 均值滤波",
        "book": "65",
        "pdf": "80",
        "figure": "ch04_mean_filter_kernel.png",
        "code": "examples/04_image_denoising/mean_filter.py",
        "concept": "均值滤波用邻域像素平均值替换中心像素，适合抑制零均值加性噪声。它本质是低通平滑，会同时削弱噪声和高频细节。",
        "formula": r"g(x,y)=\frac{1}{mn}\sum_{(i,j)\in\Omega}f(x+i,y+j)",
        "steps": ["输入灰度图和窗口大小。", "为每个像素取 m×n 邻域。", "计算邻域平均值。", "用平均值替换中心像素。", "检查噪声降低和边缘模糊的折中。"],
        "intuition": "均值滤波像让一个像素听取周围邻居的平均意见，随机噪声会被抵消，但真实边缘也会被拉平。",
        "scene": "轻微高斯噪声、预平滑、边缘检测前的粗降噪。",
        "pros": "简单、快速、易实现。",
        "limits": "容易模糊边缘和细节，对椒盐噪声不鲁棒。",
        "compare": "相较中值滤波，均值滤波对脉冲异常值敏感；相较边界保持滤波，它不会区分边缘两侧像素。",
        "links": ["[[4.2.1_均值滤波的原理]]", "[[4.2.2_均值滤波方法]]", "[[4.3_中值滤波]]", "[[5.1_图像细节的基本特征]]"],
        "review": ["均值滤波为什么能降低零均值噪声？", "窗口越大会带来什么副作用？", "均值滤波为什么容易模糊边缘？"],
    },
    "4.2.1_均值滤波的原理.md": {
        "section": "4.2.1 均值滤波的原理",
        "book": "65",
        "pdf": "80",
        "figure": "ch04_mean_filter_kernel.png",
        "code": "examples/04_image_denoising/mean_filter.py",
        "concept": "均值滤波的核心假设是噪声在局部邻域内随机起伏，而真实信号相对平稳。通过平均，随机正负扰动互相抵消，局部稳定成分被保留下来。",
        "formula": r"E\left[\frac{1}{N}\sum_{k=1}^{N}(s+n_k)\right]=s,\quad Var=\frac{\sigma^2}{N}",
        "steps": ["把邻域像素看成真实值加噪声。", "假设噪声均值接近 0。", "对 N 个邻域像素求平均。", "噪声方差随 N 增大而降低。", "注意跨边缘平均会破坏局部平稳假设。"],
        "intuition": "多次测量取平均会更稳定；均值滤波就是把附近像素当作对同一局部亮度的多次测量。",
        "scene": "局部灰度变化平缓的背景区域降噪。",
        "pros": "有清楚的统计解释。",
        "limits": "边缘和纹理区域并不满足局部平稳假设。",
        "compare": "中值滤波关注排序统计量；均值滤波关注算术平均。",
        "links": ["[[4.2_均值滤波]]", "[[4.4_边界保持类平滑滤波]]"],
        "review": ["为什么平均能降低方差？", "局部平稳假设什么时候不成立？", "均值滤波对孤立极值为什么敏感？"],
    },
    "4.2.2_均值滤波方法.md": {
        "section": "4.2.2 均值滤波方法",
        "book": "66",
        "pdf": "81",
        "figure": "ch04_mean_filter_kernel.png",
        "code": "examples/04_image_denoising/mean_filter.py",
        "concept": "均值滤波方法的实现重点是窗口形状、窗口大小、边界处理和卷积效率。窗口越大平滑越强，但细节损失越明显。",
        "formula": r"g=f*h,\quad h(i,j)=\frac{1}{mn},\ (i,j)\in\Omega",
        "steps": ["选择方形、十字形或其他邻域窗口。", "确定窗口尺寸。", "选择边界填充方式。", "用卷积或积分图快速计算局部均值。", "输出平滑结果。"],
        "intuition": "方法层面要回答：看多大范围的邻居、边缘外面怎么补、计算怎样更快。",
        "scene": "实时预处理、简单降噪基线、后续锐化或分割前的平滑。",
        "pros": "实现成本低，适合做去噪对照实验。",
        "limits": "参数单一，难以兼顾大噪声和平滑边缘。",
        "compare": "均值滤波是线性滤波；中值滤波是非线性排序滤波。",
        "links": ["[[4.2_均值滤波]]", "[[4.3.2_中值滤波方法]]", "[[5.5_Canny算子]]"],
        "review": ["边界填充会怎样影响滤波结果？", "为什么窗口大小不能无限增大？", "卷积实现和直接循环实现有什么差别？"],
    },
    "4.3_中值滤波.md": {
        "section": "4.3 中值滤波",
        "book": "69",
        "pdf": "84",
        "figure": "ch04_median_filter_window.png",
        "code": "examples/04_image_denoising/median_filter.py",
        "concept": "中值滤波用邻域排序后的中间值替换中心像素，对孤立极大或极小的脉冲噪声很有效。它是非线性滤波，常用于椒盐噪声。",
        "formula": r"g(x,y)=median\{f(x+i,y+j)\mid(i,j)\in\Omega\}",
        "steps": ["输入图像和奇数窗口大小。", "取中心像素周围邻域。", "对邻域灰度排序。", "取中间值作为输出。", "比较椒盐点是否被去除以及边缘是否保持。"],
        "intuition": "中值滤波像投票选中间意见，极端黑点或白点会被多数正常像素压下去。",
        "scene": "椒盐噪声、二值或灰度图孤立异常点清理、分割前预处理。",
        "pros": "对孤立脉冲噪声鲁棒，边缘保持通常好于均值滤波。",
        "limits": "对高斯噪声未必最优；窗口过大会破坏细小结构。",
        "compare": "均值会被极端值拉偏，中值对极端值不敏感。",
        "links": ["[[4.3.1_中值滤波的原理]]", "[[4.3.2_中值滤波方法]]", "[[7.2_腐蚀与膨胀]]"],
        "review": ["为什么中值滤波适合椒盐噪声？", "为什么窗口通常取奇数尺寸？", "中值滤波会怎样影响细线结构？"],
    },
    "4.3.1_中值滤波的原理.md": {
        "section": "4.3.1 中值滤波的原理",
        "book": "69",
        "pdf": "84",
        "figure": "ch04_median_filter_window.png",
        "code": "examples/04_image_denoising/median_filter.py",
        "concept": "中值滤波利用排序统计量的鲁棒性：只要窗口内异常值数量不超过一半，中值就更可能落在正常灰度范围内。",
        "formula": r"median(\Omega)=v_{\lceil N/2\rceil},\quad v_1\le v_2\le\cdots\le v_N",
        "steps": ["收集邻域像素。", "按灰度从小到大排序。", "取中间位置。", "用中值替代中心像素。", "分析异常点比例是否超过窗口承受范围。"],
        "intuition": "一个班里少数同学报了离谱分数，平均分会被带偏，中位数更能代表多数人。",
        "scene": "孤立点、脉冲噪声、坏点修复。",
        "pros": "对少量极端异常值稳定。",
        "limits": "排序计算比均值更复杂，纹理密集时可能过度简化。",
        "compare": "中值滤波不是线性卷积，不能简单用频率响应完全描述。",
        "links": ["[[4.3_中值滤波]]", "[[4.1_图像噪声]]"],
        "review": ["中值为什么不容易受极端值影响？", "异常点超过一半时会发生什么？", "中值滤波为什么是非线性的？"],
    },
    "4.3.2_中值滤波方法.md": {
        "section": "4.3.2 中值滤波方法",
        "book": "69",
        "pdf": "84",
        "figure": "ch04_median_filter_window.png",
        "code": "examples/04_image_denoising/median_filter.py",
        "concept": "中值滤波方法需要选择窗口尺寸和形状。小窗口保细节但去噪弱，大窗口去噪强但会抹掉细线和小目标。",
        "formula": r"g(x,y)=median_{\Omega_{m\times n}}(f)",
        "steps": ["选择 3×3、5×5 等奇数窗口。", "确定边界处理方式。", "逐像素取邻域中值。", "必要时多次迭代或与形态学处理结合。", "评估目标形状是否被改变。"],
        "intuition": "方法实现的关键是窗口要刚好覆盖噪声点，又不要大到把目标细节当作噪声删掉。",
        "scene": "扫描件黑白点清理、简单医学或工业图像坏点去除。",
        "pros": "参数直观，效果稳定。",
        "limits": "过大窗口会导致形状变钝、细节消失。",
        "compare": "相较均值滤波，中值滤波更适合椒盐噪声；相较非局部均值，它只看局部窗口。",
        "links": ["[[4.3_中值滤波]]", "[[4.5_非局部均值滤波]]"],
        "review": ["3×3 和 5×5 窗口怎么选？", "重复中值滤波有什么风险？", "中值滤波和形态学开闭运算有什么联系？"],
    },
    "4.4_边界保持类平滑滤波.md": {
        "section": "4.4 边界保持类平滑滤波",
        "book": "71",
        "pdf": "86",
        "figure": "ch04_edge_preserving_filters.png",
        "code": "examples/04_image_denoising/k_nearest_mean_filter.py",
        "concept": "边界保持类平滑滤波试图只在同一区域内部平均，避免跨越边缘把两侧灰度混在一起。K近邻均值和对称近邻均值都属于这种思想。",
        "formula": r"g(x,y)=\frac{1}{|S|}\sum_{(i,j)\in S}f(i,j),\quad S=\{p\in\Omega: |f(p)-f(x,y)|\text{较小}\}",
        "steps": ["输入图像、窗口大小和相似性规则。", "在邻域内筛选与中心像素相近的像素。", "只对筛选集合求平均。", "输出平滑结果。", "观察边缘是否比普通均值滤波更清晰。"],
        "intuition": "不要让边缘另一边的像素参与平均，就像讨论局部亮度时只听同一侧邻居的意见。",
        "scene": "既要降噪又要保边的预处理、边缘检测前平滑、工业缺陷轮廓保持。",
        "pros": "比普通均值更能保留边缘。",
        "limits": "相似性阈值或选择规则会影响稳定性，计算量较大。",
        "compare": "均值滤波跨边缘平均；边界保持滤波选择性平均。",
        "links": ["[[4.4.1_K近邻均值滤波]]", "[[4.4.2_对称近邻均值滤波]]", "[[5.4_微分算子在边缘检测中的应用]]"],
        "review": ["为什么跨边缘平均会模糊轮廓？", "边界保持滤波如何选择参与平均的像素？", "它和非局部均值的相似性思想有什么区别？"],
    },
    "4.4.1_K近邻均值滤波.md": {
        "section": "4.4.1 K近邻均值滤波",
        "book": "72",
        "pdf": "87",
        "figure": "ch04_edge_preserving_filters.png",
        "code": "examples/04_image_denoising/k_nearest_mean_filter.py",
        "concept": "K近邻均值滤波在窗口中选择与中心像素灰度最接近的 K 个像素求平均，避免明显不同区域的像素参与平滑。",
        "formula": r"S_K=\operatorname{arg\,topK}_{p\in\Omega}(-|f(p)-f_c|),\quad g=\frac{1}{K}\sum_{p\in S_K}f(p)",
        "steps": ["输入窗口大小和 K。", "计算窗口内每个像素与中心灰度差。", "选取差值最小的 K 个像素。", "对这些像素求均值。", "输出边界保持平滑结果。"],
        "intuition": "它不是平均所有邻居，而是挑最像中心像素的邻居来平均。",
        "scene": "边缘附近去噪、纹理较弱但边界清楚的图像。",
        "pros": "比普通均值滤波更少跨边缘模糊。",
        "limits": "K 过小去噪弱，K 过大又退化为普通均值。",
        "compare": "对称近邻按成对位置选择，K近邻按灰度相似性排序选择。",
        "links": ["[[4.4_边界保持类平滑滤波]]", "[[4.4.2_对称近邻均值滤波]]"],
        "review": ["K 值太大或太小分别有什么问题？", "为什么灰度相似性能帮助保边？", "K近邻均值与双边滤波思想有什么相似处？"],
    },
    "4.4.2_对称近邻均值滤波.md": {
        "section": "4.4.2 对称近邻均值滤波",
        "book": "73",
        "pdf": "88",
        "figure": "ch04_edge_preserving_filters.png",
        "code": "examples/04_image_denoising/symmetric_nearest_mean_filter.py",
        "concept": "对称近邻均值滤波把中心像素两侧对称位置成对比较，从每对中选择更接近中心灰度的像素参与平均，从而减少跨边缘采样。",
        "formula": r"q=\arg\min_{p\in\{p_1,p_2\}} |f(p)-f_c|,\quad g=\frac{1}{M}\sum q",
        "steps": ["输入窗口大小。", "围绕中心构造对称像素对。", "每对选择更接近中心灰度的一方。", "把被选像素和中心像素求平均。", "输出平滑图像。"],
        "intuition": "如果中心点在边缘一侧，对称点对里同侧那个通常更像它，另一侧会被排除。",
        "scene": "边界附近的局部平滑、轮廓保持去噪。",
        "pros": "利用空间对称关系，边界保持直观。",
        "limits": "对复杂纹理和强噪声的判断可能不稳定。",
        "compare": "K近邻均值全局排序邻域像素；对称近邻按空间成对选择。",
        "links": ["[[4.4_边界保持类平滑滤波]]", "[[4.4.1_K近邻均值滤波]]"],
        "review": ["为什么要成对比较对称像素？", "中心灰度被噪声污染时会有什么风险？", "它和普通均值滤波的根本区别是什么？"],
    },
    "4.5_非局部均值滤波.md": {
        "section": "4.5 非局部均值滤波",
        "book": "75",
        "pdf": "90",
        "figure": "ch04_non_local_means.png",
        "code": "examples/04_image_denoising/non_local_means_filter.py",
        "concept": "非局部均值滤波不只看空间邻近像素，而是在搜索窗口中寻找与参考块相似的图像块，用相似块的加权平均恢复中心像素。",
        "formula": r"g(i)=\sum_j w(i,j)f(j),\quad w(i,j)\propto \exp\left(-\frac{\|P_i-P_j\|^2}{h^2}\right)",
        "steps": ["输入参考块大小、搜索窗口和滤波强度 h。", "为每个像素提取参考块。", "在搜索窗口中计算其他块与参考块的相似度。", "根据相似度生成权重。", "用加权平均输出去噪像素。"],
        "intuition": "如果图像里有很多相似纹理块，就让这些相似块互相投票，而不是只相信附近几个像素。",
        "scene": "纹理重复图像、自然图像高质量去噪、低照度图像预处理。",
        "pros": "能利用非局部重复结构，细节保持较好。",
        "limits": "计算量较大，参数 h 和窗口大小敏感。",
        "compare": "局部滤波只看附近像素；非局部均值看相似块，空间上可以更远。",
        "links": ["[[4.1_图像噪声]]", "[[4.4_边界保持类平滑滤波]]", "[[9.3.4_应用于图像去噪]]"],
        "review": ["非局部均值中的“非局部”是什么意思？", "h 参数过大会怎样？", "为什么相似块比单个相似像素更可靠？"],
    },
    "4.x_习题.md": {
        "section": "4.x 习题",
        "book": "77",
        "pdf": "92",
        "figure": "ch04_noise_models.png",
        "code": "examples/04_image_denoising/README.md",
        "concept": "第 4 章习题应围绕噪声类型、滤波器选择、参数影响和边缘保持能力展开。复习时要能说明为什么某种噪声适合某种滤波器。",
        "formula": r"\text{去噪选择}=f(\text{噪声类型},\text{边缘保持要求},\text{计算量})",
        "steps": ["判断噪声类型。", "选择候选滤波器。", "写出核心公式。", "分析参数变化。", "用示例脚本验证。"],
        "intuition": "做去噪题的关键不是背滤波名字，而是解释噪声、边缘和滤波窗口之间的取舍。",
        "scene": "课程复习、实验报告、算法选型。",
        "pros": "把方法和噪声模型对应起来。",
        "limits": "原书习题细节需人工复核。",
        "compare": "第 4 章重噪声抑制，第 5 章重细节增强；两章经常前后衔接。",
        "links": ["[[4.1_图像噪声]]", "[[4.2_均值滤波]]", "[[4.3_中值滤波]]", "[[4.5_非局部均值滤波]]"],
        "review": ["如何根据噪声类型选择滤波器？", "去噪和锐化为什么常有矛盾？", "如何证明一个滤波器保边能力更强？"],
    },
}


def reading_block(pdf: str) -> str:
    page = pdf.split("-", 1)[0]
    return f"""> [!note] 书中对应页
> PDF 页码：{pdf}
> 打开原页（Obsidian）：[[raw/books/数字图像处理基础_朱虹.pdf#page={page}]]
>
> GitHub 公开仓库不随附原书 PDF；下载仓库后，将有权使用的同名 PDF 放入 `raw/books/`，下面的 Obsidian 本地内嵌预览才会显示。
> ![[raw/books/数字图像处理基础_朱虹.pdf#page={page}]]
"""


def source_status(profile: dict[str, object]) -> str:
    return f"""## 来源与状态

* 书名：数字图像处理基础
* 作者：朱虹
* 章节：第 4 章 图像去噪
* 小节：{profile["section"]}
* 书中页码：{profile["book"]}
* PDF 页码：{profile["pdf"]}
* 本地 PDF：raw/books/数字图像处理基础_朱虹.pdf
* 处理状态：已精修 / 需人工复核
"""


def render_note(filename: str, profile: dict[str, object]) -> str:
    steps = "\n".join(f"{i}. {item}" for i, item in enumerate(profile["steps"], 1))
    links = "\n".join(f"- {item}" for item in profile["links"])
    review = "\n".join(f"{i}. {item}" for i, item in enumerate(profile["review"], 1))
    return f"""# {Path(filename).stem}

{reading_block(profile["pdf"])}

{source_status(profile)}

## 核心概念

{profile["concept"]}

## 关键公式

```math
{profile["formula"]}
```

公式按通用图像处理记号整理；与原书符号、窗口定义或边界约定不一致处，需人工复核。

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

## 和相关方法的对比

{profile["compare"]}

## 教学图示

![{profile["section"]} 教学图示](../../assets/extracted_figures/{profile["figure"]})

该图为本仓库原创教学示意图，不是原书截图。

## 对应代码

- [{profile["code"]}](../../{profile["code"]})

## 相关知识

{links}

## 复习问题

{review}
"""


def refine_wiki() -> None:
    for filename, profile in PROFILES.items():
        (CH4 / filename).write_text(render_note(filename, profile), encoding="utf-8")
    index = "\n".join(f"- [[{Path(name).stem}]]" for name in PROFILES)
    (CH4 / "README.md").write_text(
        f"""# 图像去噪

## 章节定位

第 4 章是第 4-11 章批量精修的起点，围绕噪声模型、局部滤波、边界保持和平滑质量评估建立学习路径。

## 学习主线

1. 先判断噪声类型。
2. 再选择均值、中值、边界保持或非局部均值滤波。
3. 对比噪声抑制、边缘保持和计算量。
4. 把去噪结果连接到第 5 章锐化和第 6 章分割。

## 小节索引

{index}

## 代码入口

- [examples/04_image_denoising/README.md](../../examples/04_image_denoising/README.md)

## 教学图示

- [第 4 章原创教学图示索引](../../assets/extracted_figures/README.md)
""",
        encoding="utf-8",
    )


def update_semantic_edges() -> None:
    path = ROOT / "graph" / "semantic_edges.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    nodes = data.setdefault("nodes", [])
    edges = data.setdefault("edges", [])
    node_ids = {node["id"] for node in nodes}
    edge_keys = {(edge["source"], edge["target"], edge["type"]) for edge in edges}

    new_nodes = [
        ("formula/ch04_additive_noise", "加性噪声模型", "formula", "wiki/04_图像去噪/4.1_图像噪声.md"),
        ("formula/ch04_mean_filter", "均值滤波公式", "formula", "wiki/04_图像去噪/4.2_均值滤波.md"),
        ("formula/ch04_median_filter", "中值滤波公式", "formula", "wiki/04_图像去噪/4.3_中值滤波.md"),
        ("formula/ch04_nlm_weight", "非局部均值权重", "formula", "wiki/04_图像去噪/4.5_非局部均值滤波.md"),
        ("concept/ch04_gaussian_noise", "高斯噪声", "concept", "wiki/04_图像去噪/4.1_图像噪声.md"),
        ("concept/ch04_salt_pepper_noise", "椒盐噪声", "concept", "wiki/04_图像去噪/4.1_图像噪声.md"),
        ("examples/04_image_denoising/mean_filter.py", "mean_filter.py", "code", "examples/04_image_denoising/mean_filter.py"),
        ("examples/04_image_denoising/median_filter.py", "median_filter.py", "code", "examples/04_image_denoising/median_filter.py"),
        ("examples/04_image_denoising/k_nearest_mean_filter.py", "k_nearest_mean_filter.py", "code", "examples/04_image_denoising/k_nearest_mean_filter.py"),
        ("examples/04_image_denoising/symmetric_nearest_mean_filter.py", "symmetric_nearest_mean_filter.py", "code", "examples/04_image_denoising/symmetric_nearest_mean_filter.py"),
        ("examples/04_image_denoising/non_local_means_filter.py", "non_local_means_filter.py", "code", "examples/04_image_denoising/non_local_means_filter.py"),
    ]
    for node_id, label, node_type, node_path in new_nodes:
        if node_id not in node_ids:
            nodes.append({"id": node_id, "label": label, "type": node_type, "chapter": "04_图像去噪", "path": node_path})
            node_ids.add(node_id)

    new_edges = [
        ("wiki/04_图像去噪/4.1_图像噪声", "formula/ch04_additive_noise", "USES_FORMULA", "图像噪声用退化模型描述。"),
        ("wiki/04_图像去噪/4.2_均值滤波", "formula/ch04_mean_filter", "USES_FORMULA", "均值滤波依赖邻域平均公式。"),
        ("wiki/04_图像去噪/4.3_中值滤波", "formula/ch04_median_filter", "USES_FORMULA", "中值滤波依赖排序统计量。"),
        ("wiki/04_图像去噪/4.5_非局部均值滤波", "formula/ch04_nlm_weight", "USES_FORMULA", "非局部均值依赖相似块权重。"),
        ("concept/ch04_gaussian_noise", "wiki/04_图像去噪/4.2_均值滤波", "APPLIES_TO", "均值滤波适合轻微加性噪声。"),
        ("concept/ch04_salt_pepper_noise", "wiki/04_图像去噪/4.3_中值滤波", "APPLIES_TO", "中值滤波适合椒盐噪声。"),
        ("wiki/04_图像去噪/4.2_均值滤波", "wiki/04_图像去噪/4.3_中值滤波", "COMPARES_WITH", "均值滤波对极值敏感，中值滤波对脉冲噪声鲁棒。"),
        ("wiki/04_图像去噪/4.4_边界保持类平滑滤波", "wiki/04_图像去噪/4.2_均值滤波", "IMPROVES_OR_EXTENDS", "边界保持滤波改进普通均值跨边缘平均的问题。"),
        ("wiki/04_图像去噪/4.5_非局部均值滤波", "wiki/04_图像去噪/4.4_边界保持类平滑滤波", "IMPROVES_OR_EXTENDS", "非局部均值把相似性从局部邻域扩展到相似块搜索。"),
        ("wiki/04_图像去噪/4.1_图像噪声", "wiki/04_图像去噪/4.2_均值滤波", "PREREQUISITE", "选择均值滤波前需要判断噪声模型。"),
        ("wiki/04_图像去噪/4.2_均值滤波", "wiki/05_图像锐化/5.5_Canny算子", "PREREQUISITE", "Canny 边缘检测通常先平滑降噪。"),
        ("wiki/04_图像去噪/4.4_边界保持类平滑滤波", "wiki/04_图像去噪/4.4.1_K近邻均值滤波", "GENERALIZES", "边界保持类方法包含 K近邻均值滤波。"),
        ("wiki/04_图像去噪/4.4_边界保持类平滑滤波", "wiki/04_图像去噪/4.4.2_对称近邻均值滤波", "GENERALIZES", "边界保持类方法包含对称近邻均值滤波。"),
        ("wiki/04_图像去噪/4.2_均值滤波", "examples/04_image_denoising/mean_filter.py", "IMPLEMENTED_BY", "均值滤波示例代码。"),
        ("wiki/04_图像去噪/4.3_中值滤波", "examples/04_image_denoising/median_filter.py", "IMPLEMENTED_BY", "中值滤波示例代码。"),
        ("wiki/04_图像去噪/4.4.1_K近邻均值滤波", "examples/04_image_denoising/k_nearest_mean_filter.py", "IMPLEMENTED_BY", "K近邻均值滤波示例代码。"),
        ("wiki/04_图像去噪/4.4.2_对称近邻均值滤波", "examples/04_image_denoising/symmetric_nearest_mean_filter.py", "IMPLEMENTED_BY", "对称近邻均值滤波示例代码。"),
        ("wiki/04_图像去噪/4.5_非局部均值滤波", "examples/04_image_denoising/non_local_means_filter.py", "IMPLEMENTED_BY", "非局部均值滤波示例代码。"),
    ]
    for source, target, rel_type, description in new_edges:
        key = (source, target, rel_type)
        if key not in edge_keys:
            edges.append({"source": source, "target": target, "type": rel_type, "description": description})
            edge_keys.add(key)

    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def update_docs() -> None:
    coverage = ROOT / "coverage_report.md"
    text = coverage.read_text(encoding="utf-8")
    marker = "## 第 4 章处理记录"
    block = """## 第 4 章处理记录

- 处理的 wiki 文件：`4.1_图像噪声.md`、`4.2_均值滤波.md`、`4.2.1_均值滤波的原理.md`、`4.2.2_均值滤波方法.md`、`4.3_中值滤波.md`、`4.3.1_中值滤波的原理.md`、`4.3.2_中值滤波方法.md`、`4.4_边界保持类平滑滤波.md`、`4.4.1_K近邻均值滤波.md`、`4.4.2_对称近邻均值滤波.md`、`4.5_非局部均值滤波.md`、`4.x_习题.md`。
- 新增原创教学图示：`ch04_noise_models.png`、`ch04_mean_filter_kernel.png`、`ch04_median_filter_window.png`、`ch04_edge_preserving_filters.png`、`ch04_non_local_means.png`。
- 优化代码：`mean_filter.py`、`median_filter.py`、`k_nearest_mean_filter.py`、`symmetric_nearest_mean_filter.py`、`non_local_means_filter.py`，并新增第 4 章 `_utils.py`。
- 新增图谱关系：噪声模型到滤波方法的 `APPLIES_TO`，均值/中值对比的 `COMPARES_WITH`，边界保持和非局部均值的 `IMPROVES_OR_EXTENDS`，以及公式与代码实现关系。
- 仍需人工复核：原书公式编号、窗口符号、页码边界和个别算法细节。
- 未完成内容：未加入原书截图和原始文本，原因是公开仓库需规避版权风险；后续可继续增加原创实验图和更多定量指标。
"""
    if marker in text:
        text = text.split(marker, 1)[0].rstrip() + "\n\n" + block
    else:
        text = text.rstrip() + "\n\n" + block
    coverage.write_text(text, encoding="utf-8")

    readme = ROOT / "README.md"
    readme_text = readme.read_text(encoding="utf-8")
    readme_text = readme_text.replace(
        "- 第 4 章到第 11 章已按模板升级为结构化精修初版，后续可按第 2/3 章样板继续深化。",
        "- 第 4 章“图像去噪”已升级为精品样板，包含原创图示、独立代码示例和语义图谱关系。\n- 第 5 章到第 11 章已按模板升级为结构化精修初版，后续继续在同一分支深化。",
    )
    if "python examples/04_image_denoising/mean_filter.py --kernel-size 5" not in readme_text:
        readme_text = readme_text.replace(
            "第 3 章几何变换示例：",
            "第 3 章几何变换示例：",
        )
        readme_text += "\n\n第 4 章图像去噪示例：\n\n```powershell\npython examples/04_image_denoising/mean_filter.py --kernel-size 5\npython examples/04_image_denoising/median_filter.py --kernel-size 5\npython examples/04_image_denoising/non_local_means_filter.py --h 10\n```\n"
    readme.write_text(readme_text, encoding="utf-8")

    terms = ROOT / "wiki" / "99_术语表.md"
    terms_text = terms.read_text(encoding="utf-8")
    if "## 图像去噪" not in terms_text:
        terms_text += """\n## 图像去噪\n\n- 高斯噪声：连续随机扰动，常用加性噪声模型近似。\n- 椒盐噪声：孤立黑白脉冲点，中值滤波通常更有效。\n- 均值滤波：用邻域平均抑制零均值噪声，但会模糊边缘。\n- 中值滤波：用排序中值抑制脉冲噪声，是非线性滤波。\n- 边界保持滤波：选择性平均同侧或相似像素，减少跨边缘模糊。\n- 非局部均值：用相似图像块加权平均，利用重复纹理去噪。\n"""
    terms.write_text(terms_text, encoding="utf-8")


def main() -> None:
    refine_wiki()
    update_semantic_edges()
    update_docs()
    print("Refined chapter 4 denoising content.")


if __name__ == "__main__":
    main()
