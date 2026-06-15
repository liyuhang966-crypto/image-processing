# 第 5 章 图像锐化代码示例

这些脚本默认使用 `assets/sample_images/sample_gray.png`，输出写入 `examples/output/`。

```powershell
python examples/05_image_sharpening/roberts_operator.py --scale 1.0
python examples/05_image_sharpening/sobel_operator.py --kernel-size 3 --direction both
python examples/05_image_sharpening/prewitt_operator.py --direction both
python examples/05_image_sharpening/laplacian_operator.py --amount 0.7 --kernel-size 3
python examples/05_image_sharpening/canny_edge_detection.py --low 60 --high 160
python examples/05_image_sharpening/log_filter.py --sigma 1.2 --kernel-size 5
```

所有输入图片均为可自由提交的合成样例，不使用原书图片。
