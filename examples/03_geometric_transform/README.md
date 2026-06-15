# 03_geometric_transform

本目录保存第 3 章“图像几何变换”的独立教学示例。所有示例默认使用 `assets/sample_images/sample_gray.png`，不使用原书图片。

## 运行示例

```powershell
python examples/03_geometric_transform/image_translation.py --dx 30 --dy 20
python examples/03_geometric_transform/image_mirror.py --axis horizontal
python examples/03_geometric_transform/image_rotation.py --angle 30 --interpolation linear
python examples/03_geometric_transform/image_resize.py --scale-x 0.75 --scale-y 0.75 --interpolation area
python examples/03_geometric_transform/image_shear.py --shear-x 0.25
python examples/03_geometric_transform/affine_transform.py --dx 18 --dy 12 --angle 12
python examples/03_geometric_transform/geometric_correction.py --strength 0.18
```

输出默认写入 `examples/output/`，该目录已被 `.gitignore` 忽略。
