# 第 6 章 图像分割代码示例

这些脚本默认使用 `assets/sample_images/sample_segments.png`，输出写入 `examples/output/`。

```powershell
python examples/06_image_segmentation/threshold_segmentation.py --threshold 128
python examples/06_image_segmentation/max_entropy_threshold.py
python examples/06_image_segmentation/otsu_threshold.py
python examples/06_image_segmentation/region_growing.py --seed-x 85 --seed-y 120 --tolerance 28
```

所有输入图片均为可自由提交的合成样例，不使用原书图片。
