"""Refine chapter 3 as the second high-quality sample chapter."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CH2 = ROOT / "wiki" / "02_图像增强"
CH3 = ROOT / "wiki" / "03_图像几何变换"
PDF_PATH = "raw/books/数字图像处理基础_朱虹.pdf"


CH3 = ROOT / "wiki" / "03_图像几何变换"

CH3_PROFILES = {
    "3.1_图像的位置变换.md": {
        "section": "3.1 图像的位置变换",
        "book": "43",
        "pdf": "58",
        "figure": "ch03_translation_grid.png",
        "code": "examples/03_geometric_transform/image_translation.py",
        "concept": "位置变换只改变像素在平面中的位置，不主动改变像素灰度。平移、镜像和旋转都可以看成把输出图像中的坐标反查到输入图像，再通过插值取得灰度。",
        "formula": r"\begin{bmatrix}x'\\y'\\1\end{bmatrix}=T\begin{bmatrix}x\\y\\1\end{bmatrix},\quad g(x',y')=f(x,y)",
        "steps": ["输入原图和位置变换参数。", "建立从源坐标到目标坐标的变换矩阵。", "实际计算时常用反向映射：遍历输出像素，反查输入坐标。", "对非整数坐标使用最近邻或双线性插值。", "输出与原图同尺寸或指定尺寸的变换结果。"],
        "intuition": "把图像想成画在透明胶片上的格子：位置变换是在移动、翻面或旋转胶片，格子里的灰度值本身不因为移动而变亮或变暗。",
        "scene": "图像配准、目标对齐、数据增强、扫描件方向校正和视觉检测前的几何标准化。",
        "pros": "模型清晰，矩阵形式统一，容易组合多个变换。",
        "limits": "会产生空洞、裁剪和插值误差；旋转等操作可能引入边界填充。",
        "compare": "位置变换与灰度增强不同：前者改坐标，后者改像素值。平移只加偏移，旋转还依赖角度和旋转中心。",
        "links": ["[[3.1.1_图像的平移]]", "[[3.1.2_图像的镜像]]", "[[3.1.3_图像的旋转]]", "[[3.3_齐次坐标与图像的仿射变换]]"],
        "review": ["为什么位置变换通常不改变灰度含义？", "前向映射为什么可能出现空洞？", "反向映射中为什么需要插值？", "平移、镜像、旋转的共同点是什么？"],
    },
    "3.1.1_图像的平移.md": {
        "section": "3.1.1 图像的平移",
        "book": "43",
        "pdf": "58",
        "figure": "ch03_translation_grid.png",
        "code": "examples/03_geometric_transform/image_translation.py",
        "concept": "图像平移把每个像素坐标整体加上固定偏移量，形状、大小和方向保持不变。它是最简单的仿射变换，也是理解齐次坐标的入口。",
        "formula": r"x'=x+\Delta x,\quad y'=y+\Delta y,\quad \begin{bmatrix}x'\\y'\\1\end{bmatrix}=\begin{bmatrix}1&0&\Delta x\\0&1&\Delta y\\0&0&1\end{bmatrix}\begin{bmatrix}x\\y\\1\end{bmatrix}",
        "steps": ["输入原图、水平位移 dx、垂直位移 dy。", "构造平移矩阵。", "用反向映射遍历输出图像位置。", "越界坐标用常数、复制边界或透明背景填充。", "得到平移后的图像。"],
        "intuition": "平移就是把整张图片往右、左、上或下推一段距离；新露出的区域需要用某种边界值补上。",
        "scene": "目标对齐、图像拼接前粗配准、训练数据增强、校正扫描图像的偏移。",
        "pros": "参数少、计算快、几何意义清楚。",
        "limits": "平移后边界会丢失部分内容，也会出现新空白区域。",
        "compare": "平移只改变位置，不改变方向；旋转会改变方向；缩放会改变尺寸。",
        "links": ["[[3.1_图像的位置变换]]", "[[3.3_齐次坐标与图像的仿射变换]]", "[[3.4_图像几何畸变的校正]]"],
        "review": ["dx、dy 的正负号如何影响移动方向？", "平移矩阵为什么需要齐次坐标才能写成矩阵乘法？", "边界填充值会怎样影响视觉结果？"],
    },
    "3.1.2_图像的镜像.md": {
        "section": "3.1.2 图像的镜像",
        "book": "44",
        "pdf": "59",
        "figure": "ch03_mirror_transform.png",
        "code": "examples/03_geometric_transform/image_mirror.py",
        "concept": "镜像变换把图像相对于某条轴翻转，水平镜像交换左右，垂直镜像交换上下。灰度值不变，但空间方位发生反向。",
        "formula": r"\text{水平镜像: }x'=W-1-x,\ y'=y;\quad \text{垂直镜像: }x'=x,\ y'=H-1-y",
        "steps": ["输入原图和镜像轴类型。", "根据宽度或高度计算对称坐标。", "将输出位置映射回输入位置。", "生成水平、垂直或双轴镜像图。"],
        "intuition": "镜像像把图像放到镜子前：像素到镜像轴的距离保持不变，但左右或上下顺序反过来。",
        "scene": "数据增强、相机坐标系转换、纠正左右颠倒的图像显示。",
        "pros": "无需插值，通常不会产生灰度模糊。",
        "limits": "会改变目标朝向，某些有方向语义的任务不能随意镜像。",
        "compare": "镜像和旋转都改变方向；镜像会改变手性，旋转保持手性。",
        "links": ["[[3.1_图像的位置变换]]", "[[3.1.3_图像的旋转]]", "[[3.3_齐次坐标与图像的仿射变换]]"],
        "review": ["水平镜像和垂直镜像的坐标公式有什么区别？", "为什么镜像一般不需要灰度插值？", "哪些识别任务不适合随意镜像？"],
    },
    "3.1.3_图像的旋转.md": {
        "section": "3.1.3 图像的旋转",
        "book": "45",
        "pdf": "60",
        "figure": "ch03_rotation_center.png",
        "code": "examples/03_geometric_transform/image_rotation.py",
        "concept": "旋转变换让图像围绕指定中心按角度转动。除 90 度等特殊情况外，输出像素通常落在输入的非整数坐标上，因此插值质量很关键。",
        "formula": r"\begin{bmatrix}x'\\y'\end{bmatrix}=\begin{bmatrix}\cos\theta&-\sin\theta\\\sin\theta&\cos\theta\end{bmatrix}\begin{bmatrix}x-c_x\\y-c_y\end{bmatrix}+\begin{bmatrix}c_x\\c_y\end{bmatrix}",
        "steps": ["输入旋转角度、旋转中心和缩放因子。", "把坐标平移到旋转中心附近。", "应用旋转矩阵。", "把坐标平移回图像坐标系。", "对非整数坐标插值并处理边界。"],
        "intuition": "旋转不是简单交换行列，而是每个点围绕中心走圆弧；点转完后很少正好落在像素格中心。",
        "scene": "扫描件校正、目标姿态归一化、数据增强、遥感影像方向配准。",
        "pros": "能处理方向不一致问题，矩阵形式清晰。",
        "limits": "可能裁剪边角，插值会带来轻微模糊。",
        "compare": "平移只改变原点位置；旋转依赖中心和角度；仿射变换可以同时包含旋转、平移、缩放和错切。",
        "links": ["[[3.1_图像的位置变换]]", "[[3.3_齐次坐标与图像的仿射变换]]", "[[3.2.2_图像的放大]]"],
        "review": ["旋转中心改变会怎样影响结果？", "为什么旋转后边角容易被裁剪？", "最近邻和双线性插值在旋转图上有什么视觉差异？"],
    },
    "3.2_图像的形状变换.md": {
        "section": "3.2 图像的形状变换",
        "book": "50",
        "pdf": "65",
        "figure": "ch03_resize_interpolation.png",
        "code": "examples/03_geometric_transform/image_resize.py",
        "concept": "形状变换会改变图像目标的尺寸或几何外形，包括缩小、放大和错切。它不仅改变位置，也改变像素之间的空间采样关系。",
        "formula": r"x'=s_xx,\quad y'=s_yy;\quad x'=x+k_xy\ \text{(shear)}",
        "steps": ["输入缩放或错切参数。", "确定输出图像尺寸。", "建立输出坐标到输入坐标的反向映射。", "选择插值方法完成重采样。", "输出变形后的图像。"],
        "intuition": "形状变换像拉伸、压缩或推斜一张网格纸；网格变了，像素采样密度也跟着变。",
        "scene": "图像尺寸标准化、金字塔处理、目标形变增强、透视和仿射近似处理。",
        "pros": "能适配算法输入尺寸，也能模拟目标尺度和形变变化。",
        "limits": "缩小可能混叠，放大可能模糊，错切可能扩大画布并产生空白。",
        "compare": "缩小减少采样点，放大需要补估新像素；错切改变形状但保持平行线平行。",
        "links": ["[[3.2.1_图像的缩小]]", "[[3.2.2_图像的放大]]", "[[3.2.3_图像的错切]]", "[[3.3_齐次坐标与图像的仿射变换]]"],
        "review": ["形状变换和位置变换的区别是什么？", "缩小为什么需要关注混叠？", "错切为什么属于仿射变换？"],
    },
    "3.2.1_图像的缩小.md": {
        "section": "3.2.1 图像的缩小",
        "book": "50",
        "pdf": "65",
        "figure": "ch03_resize_interpolation.png",
        "code": "examples/03_geometric_transform/image_resize.py",
        "concept": "图像缩小把多个源像素的信息压到更少的输出像素中，本质是降采样。若直接抽点，容易丢失细节或产生混叠。",
        "formula": r"x=\frac{x'}{s_x},\quad y=\frac{y'}{s_y},\quad 0<s_x,s_y<1",
        "steps": ["输入缩放比例。", "计算输出尺寸。", "必要时先低通平滑以抑制混叠。", "按反向映射找到源图坐标。", "用区域插值或双线性插值得到输出。"],
        "intuition": "缩小像把更多格子压成更少格子，不能只随便挑一个代表，否则细线和纹理可能消失或变成假花纹。",
        "scene": "生成缩略图、构建图像金字塔、降低计算量、统一模型输入尺寸。",
        "pros": "节省存储和计算，便于多尺度处理。",
        "limits": "不可避免丢失高频细节，处理不当会产生混叠。",
        "compare": "缩小推荐区域插值或预滤波；放大更关注新像素估计的平滑程度。",
        "links": ["[[3.2_图像的形状变换]]", "[[3.2.2_图像的放大]]", "[[9.1_图像的频域变换（傅里叶变换）]]"],
        "review": ["为什么缩小前常需要低通滤波？", "区域插值为什么适合缩小？", "缩小会丢失哪些信息？"],
    },
    "3.2.2_图像的放大.md": {
        "section": "3.2.2 图像的放大",
        "book": "53",
        "pdf": "68",
        "figure": "ch03_resize_interpolation.png",
        "code": "examples/03_geometric_transform/image_resize.py",
        "concept": "图像放大把较少的源像素扩展到更多输出像素，需要估计原图中不存在的新采样点。插值方法决定锯齿、模糊和边缘连续性。",
        "formula": r"g(x',y')=(1-a)(1-b)f(i,j)+a(1-b)f(i+1,j)+(1-a)bf(i,j+1)+abf(i+1,j+1)",
        "steps": ["输入放大比例。", "计算输出尺寸。", "对每个输出像素反查源图浮点坐标。", "用最近邻、双线性或三次插值估计灰度。", "输出放大图并检查边缘质量。"],
        "intuition": "放大不是凭空增加真实细节，而是在已有像素之间估计过渡值。",
        "scene": "显示缩放、标注检查、预处理到固定输入尺寸、简单超分辨率基线。",
        "pros": "实现简单，能快速适配显示或模型尺寸。",
        "limits": "不能恢复真实高频细节，可能产生模糊或块状锯齿。",
        "compare": "最近邻保边但块状明显；双线性平滑但可能模糊；深度超分辨率能学习细节但需要数据。",
        "links": ["[[3.2_图像的形状变换]]", "[[3.2.1_图像的缩小]]", "[[11.2_超分辨率图像重建卷积网络]]"],
        "review": ["放大是否真的增加图像信息？", "双线性插值为什么比最近邻更平滑？", "放大和超分辨率有什么区别？"],
    },
    "3.2.3_图像的错切.md": {
        "section": "3.2.3 图像的错切",
        "book": "56",
        "pdf": "71",
        "figure": "ch03_shear_transform.png",
        "code": "examples/03_geometric_transform/image_shear.py",
        "concept": "错切变换让图像沿某一方向按另一坐标成比例偏移，矩形会变成平行四边形，平行线仍保持平行。",
        "formula": r"x'=x+k_xy,\quad y'=y\quad \text{或}\quad x'=x,\ y'=y+k_yx",
        "steps": ["输入 x 或 y 方向错切系数。", "构造错切矩阵。", "估计输出画布范围。", "用反向映射和插值生成结果。", "处理新增空白区域。"],
        "intuition": "错切像推桌面上的一叠纸：底边不动，上边被横向推开。",
        "scene": "文档倾斜模拟、字符形变增强、仿射配准中的局部形变近似。",
        "pros": "参数少，可表示常见倾斜形变。",
        "limits": "错切不能表达透视汇聚，过大时会带来明显空白和裁剪。",
        "compare": "错切是仿射变换的特殊形式；透视变换能让平行线汇聚，错切不能。",
        "links": ["[[3.2_图像的形状变换]]", "[[3.3_齐次坐标与图像的仿射变换]]", "[[3.4_图像几何畸变的校正]]"],
        "review": ["错切后平行线是否仍平行？", "错切系数越大，输出画布会发生什么变化？", "错切和透视变换有什么边界？"],
    },
    "3.3_齐次坐标与图像的仿射变换.md": {
        "section": "3.3 齐次坐标与图像的仿射变换",
        "book": "58",
        "pdf": "73",
        "figure": "ch03_affine_transform.png",
        "code": "examples/03_geometric_transform/affine_transform.py",
        "concept": "齐次坐标把平移也写进矩阵乘法，使平移、旋转、缩放和错切能统一为一个 3×3 矩阵。仿射变换保持直线和平行关系，是第 3 章的组织核心。",
        "formula": r"\begin{bmatrix}x'\\y'\\1\end{bmatrix}=\begin{bmatrix}a&b&t_x\\c&d&t_y\\0&0&1\end{bmatrix}\begin{bmatrix}x\\y\\1\end{bmatrix}",
        "steps": ["把二维坐标扩展为齐次坐标。", "按任务构造仿射矩阵。", "组合多个矩阵时注意乘法顺序。", "用反向映射得到源图坐标。", "插值并输出仿射变换图。"],
        "intuition": "齐次坐标像给二维点多加一个工具位，让“加偏移”和“乘矩阵”放进同一种写法。",
        "scene": "图像配准、目标姿态归一化、数据增强、文档校正的仿射近似。",
        "pros": "表达统一，便于组合和求逆；平移、旋转、缩放、错切都可纳入同一框架。",
        "limits": "不能表达所有透视畸变或复杂非线性畸变。",
        "compare": "平移、旋转、缩放、错切都是仿射的特殊形式；几何畸变校正常常需要更一般的非线性映射。",
        "links": ["[[3.1.1_图像的平移]]", "[[3.1.3_图像的旋转]]", "[[3.2.3_图像的错切]]", "[[3.4_图像几何畸变的校正]]"],
        "review": ["为什么普通 2×2 矩阵不能直接表示平移？", "仿射变换保持哪些几何性质？", "多个变换矩阵组合时为什么顺序重要？", "仿射和透视变换的差别是什么？"],
    },
    "3.4_图像几何畸变的校正.md": {
        "section": "3.4 图像几何畸变的校正",
        "book": "59",
        "pdf": "74",
        "figure": "ch03_geometric_correction.png",
        "code": "examples/03_geometric_transform/geometric_correction.py",
        "concept": "几何畸变校正根据畸变模型或控制点，把弯曲、倾斜或非线性偏移的图像坐标映射回理想坐标。它依赖坐标映射、插值和边界处理。",
        "formula": r"(x_s,y_s)=F^{-1}(x_d,y_d),\quad g(x_d,y_d)=f(x_s,y_s)",
        "steps": ["识别畸变类型或采集控制点。", "估计从校正图到原图的反向映射。", "遍历输出图像坐标并查找源图位置。", "对源图浮点坐标插值。", "评估直线、网格或标定点是否恢复合理。"],
        "intuition": "校正不是简单把图像拉直，而是为输出图每个位置找到它在畸变原图中对应的来源。",
        "scene": "镜头畸变校正、扫描件校正、遥感几何校正、工业相机标定后的图像标准化。",
        "pros": "能补偿成像系统或拍摄姿态导致的几何误差。",
        "limits": "依赖模型或控制点质量；错误映射会造成局部拉伸、压缩和插值伪影。",
        "compare": "仿射变换处理全局线性几何关系；畸变校正可以是非线性坐标映射。",
        "links": ["[[3.3_齐次坐标与图像的仿射变换]]", "[[3.1_图像的位置变换]]", "[[3.2_图像的形状变换]]"],
        "review": ["为什么几何畸变校正常用反向映射？", "控制点误差会怎样影响校正结果？", "仿射校正和径向畸变校正适用场景有何不同？"],
    },
    "3.x_习题.md": {
        "section": "3.x 习题",
        "book": "62",
        "pdf": "77",
        "figure": "ch03_affine_transform.png",
        "code": "examples/03_geometric_transform/README.md",
        "concept": "本页把第 3 章习题整理为复习任务：能写出坐标公式、解释插值选择、判断变换类别，并用代码复现实验现象。",
        "formula": r"\text{几何变换复习主线：坐标映射}\rightarrow\text{反向采样}\rightarrow\text{插值}\rightarrow\text{边界处理}",
        "steps": ["先判断题目属于平移、镜像、旋转、缩放、错切、仿射还是畸变校正。", "写出对应坐标公式或矩阵。", "说明输出坐标如何反查输入坐标。", "选择插值方法并解释原因。", "用示例代码验证一个最小案例。"],
        "intuition": "做第 3 章题时，不要只记公式名；先问自己：输出图上这个像素从原图哪里来？",
        "scene": "期末复习、实验报告、代码调试和知识图谱回顾。",
        "pros": "把公式、图示和代码连在一起，便于查漏补缺。",
        "limits": "习题原文和个别页码仍需对照本地合法 PDF 复核。",
        "compare": "第 3 章题目重坐标关系；第 2 章题目重灰度映射，两者常在预处理中连续使用。",
        "links": ["[[3.1_图像的位置变换]]", "[[3.2_图像的形状变换]]", "[[3.3_齐次坐标与图像的仿射变换]]", "[[3.4_图像几何畸变的校正]]"],
        "review": ["看到几何变换题，第一步应判断什么？", "为什么插值方法会影响视觉效果？", "如何用合成网格图验证平移或旋转？", "第 3 章与第 2 章增强方法在处理对象上有什么根本不同？"],
    },
}


def preserve_reading_block(text: str) -> str:
    if text.startswith("> [!note]"):
        match = re.search(r"\n## ", text)
        if match:
            return text[: match.start()].rstrip() + "\n\n"
    return ""


def reading_block(pdf: str) -> str:
    page = pdf.split("-", 1)[0]
    return f"""> [!note] 书中对应页
> PDF 页码：{pdf}
> 打开原页（Obsidian）：[[{PDF_PATH}#page={page}]]
>
> GitHub 公开仓库不随附原书 PDF；下载仓库后，将有权使用的同名 PDF 放入 `raw/books/`，下面的 Obsidian 本地内嵌预览才会显示。
> ![[{PDF_PATH}#page={page}]]
"""


def source_status(section: str, book: str, pdf: str) -> str:
    return f"""## 来源与状态

* 书名：数字图像处理基础
* 作者：朱虹
* 章节：第 3 章 图像几何变换
* 小节：{section}
* 书中页码：{book}
* PDF 页码：{pdf}
* 本地 PDF：{PDF_PATH}
* 处理状态：已精修 / 需人工复核
"""


def render_note(path: Path, profile: dict[str, object]) -> str:
    steps = "\n".join(f"{i}. {item}" for i, item in enumerate(profile["steps"], 1))
    links = "\n".join(f"- {item}" for item in profile["links"])
    review = "\n".join(f"{i}. {item}" for i, item in enumerate(profile["review"], 1))
    return f"""# {path.stem}

{reading_block(profile["pdf"])}

{source_status(profile["section"], profile["book"], profile["pdf"])}

## 核心概念

{profile["concept"]}

## 关键公式

```math
{profile["formula"]}
```

公式按通用图像处理记号整理；若与原书符号、坐标原点或旋转方向约定不完全一致，需人工复核。

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


def refine_chapter3() -> None:
    for filename, profile in CH3_PROFILES.items():
        (CH3 / filename).write_text(render_note(CH3 / filename, profile), encoding="utf-8")

    index = "\n".join(f"- [[{Path(name).stem}]]" for name in CH3_PROFILES)
    (CH3 / "README.md").write_text(
        f"""# 图像几何变换

## 章节定位

第 3 章是本知识库的第二个精品样板章节，重点围绕坐标映射、反向采样、插值和几何校正建立学习路径。

## 学习主线

1. 先理解位置变换：平移、镜像、旋转。
2. 再理解形状变换：缩小、放大、错切。
3. 用齐次坐标把基本变换统一为仿射矩阵。
4. 最后把坐标映射思想扩展到几何畸变校正。

## 小节索引

{index}

## 代码入口

- [examples/03_geometric_transform/README.md](../../examples/03_geometric_transform/README.md)

## 教学图示

- [第 3 章原创教学图示索引](../../assets/extracted_figures/README.md)
""",
        encoding="utf-8",
    )


def infer_ch2_source(path: Path, text: str) -> str:
    pdf_match = re.search(r"PDF 页码：(\d+)", text)
    pdf = pdf_match.group(1) if pdf_match else "需人工复核"
    book = str(int(pdf) - 15) if pdf.isdigit() else "需人工复核"
    return f"""## 来源与状态

* 书名：数字图像处理基础
* 作者：朱虹
* 章节：第 2 章 图像增强
* 小节：{path.stem.replace("_", " ")}
* 书中页码：{book}
* PDF 页码：{pdf}
* 本地 PDF：{PDF_PATH}
* 处理状态：已精修 / 需人工复核
"""


def ensure_ch2_standard_sections() -> None:
    figure_map = {
        "2.1": "ch02_gamma_curves.png",
        "2.2": "ch02_contrast_stretching.png",
        "2.3": "ch02_gray_window_slicing.png",
        "2.3.1": "ch02_gray_window_slicing.png",
        "2.3.2": "ch02_gray_window_slicing.png",
        "2.4": "ch02_contrast_stretching.png",
        "2.4.1": "ch02_contrast_stretching.png",
        "2.4.2": "ch02_gamma_curves.png",
        "2.5": "ch02_histogram_equalization.png",
        "2.6": "ch02_adaptive_histogram_equalization.png",
        "2.7": "ch02_pseudo_color_lut.png",
        "2.8": "ch02_retinex_decomposition.png",
        "2.x": "ch02_histogram_equalization.png",
    }
    code_map = {
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
        "2.x": "examples/02_image_enhancement/README.md",
    }
    for path in sorted(CH2.glob("*.md")):
        if path.name == "README.md":
            continue
        text = path.read_text(encoding="utf-8")
        prefix = path.stem.split("_", 1)[0]
        title = f"# {path.stem}"
        text_without_title = re.sub(r"^# .+\n+", "", text, count=1, flags=re.M)
        pdf_match = re.search(r"PDF 页码：([0-9-]+)", text)
        pdf = pdf_match.group(1) if pdf_match else "需人工复核"
        block = reading_block(pdf if pdf != "需人工复核" else "需人工复核")
        body = re.sub(r"> \[!note\] 书中对应页\n(?:>.*\n?)+\n?", "", text_without_title, count=1)
        body = re.sub(
            r"## 来源与状态\n(?:.|\n)*?(?=\n## |\n# |\Z)",
            "",
            body,
            count=1,
        ).lstrip()
        if "## 来源与状态" not in body:
            body = infer_ch2_source(path, text).rstrip() + "\n\n" + body
        if "## 教学图示" not in body:
            figure = figure_map[prefix]
            body += f"\n\n## 教学图示\n\n![{path.stem} 教学图示](../../assets/extracted_figures/{figure})\n\n该图为本仓库原创教学示意图，不是原书截图。\n"
        if "## 对应代码" not in body:
            code = code_map[prefix]
            body += f"\n\n## 对应代码\n\n- [{code}](../../{code})\n"
        if prefix == "2.x":
            if "## 核心概念" not in body:
                body += "\n\n## 核心概念\n\n第 2 章习题用于检查图像增强方法的选择逻辑：先判断问题是灰度映射、直方图调整、伪彩色显示还是照明校正，再说明参数和副作用。\n"
            if "## 关键公式" not in body:
                body += "\n\n## 关键公式\n\n```math\ns=T(r),\\quad p_r(r_k)=\\frac{n_k}{MN},\\quad s_k=(L-1)\\sum_{j=0}^{k}p_r(r_j)\n```\n\n公式覆盖灰度映射和直方图均衡化的复习主线；题目中的具体符号需人工复核。\n"
            if "## 算法步骤" not in body:
                body += "\n\n## 算法步骤\n\n1. 判断图像主要问题：偏暗、低对比、目标灰度范围窄、局部对比不足或照明不均。\n2. 选择对应增强方法并写出核心映射。\n3. 说明参数如何影响输出。\n4. 分析可能的过增强、噪声放大或颜色误读。\n5. 用代码示例验证至少一个输入输出现象。\n"
            if "## 相关知识" not in body:
                body += "\n\n## 相关知识\n\n- [[2.1_γ校正]]\n- [[2.2_对比度线性展宽]]\n- [[2.5_直方图均衡化]]\n- [[2.6_自适应直方图均衡化]]\n- [[2.8_Retinex图像增强方法]]\n"
            if "## 复习问题" not in body:
                body += "\n\n## 复习问题\n\n1. 如何区分 γ校正、线性展宽和直方图均衡化的适用场景？\n2. 为什么 CLAHE 通常比全局均衡更适合局部对比不足图像？\n3. 伪彩色为什么不能被理解为增加了图像信息？\n4. Retinex 与普通灰度映射的核心差异是什么？\n"
        path.write_text((title + "\n\n" + block + "\n" + body).strip() + "\n", encoding="utf-8")


def main() -> None:
    refine_chapter3()
    ensure_ch2_standard_sections()
    print("Refined chapter 3 and normalized chapter 2 source/status sections.")


if __name__ == "__main__":
    main()
