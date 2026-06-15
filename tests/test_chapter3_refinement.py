import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_module(path: Path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class Chapter3ExampleTest(unittest.TestCase):
    def test_geometric_examples_expose_independent_core_functions(self):
        expected = {
            "image_translation.py": "translate_image",
            "image_mirror.py": "mirror_image",
            "image_rotation.py": "rotate_image",
            "image_resize.py": "resize_image",
            "image_shear.py": "shear_image",
            "affine_transform.py": "affine_transform_image",
            "geometric_correction.py": "correct_geometric_distortion",
        }
        folder = ROOT / "examples" / "03_geometric_transform"

        for filename, function_name in expected.items():
            with self.subTest(filename=filename):
                module = load_module(folder / filename)
                self.assertTrue(
                    callable(getattr(module, function_name, None)),
                    f"{filename} should define {function_name}()",
                )


class CoverageToolTest(unittest.TestCase):
    def test_check_coverage_declares_chapter_3_requirements(self):
        module = load_module(ROOT / "tools" / "check_coverage.py")

        self.assertIn("3.1.1_图像的平移.md", module.REQUIRED_CHAPTER3_WIKI)
        self.assertIn("ch03_translation_grid.png", module.REQUIRED_CHAPTER3_FIGURES)
        self.assertIn("image_translation.py", module.REQUIRED_CHAPTER3_CODE)


if __name__ == "__main__":
    unittest.main()
