import importlib.util
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_module(path: Path):
    previous_utils = sys.modules.pop("_utils", None)
    previous_path = list(sys.path)
    sys.path.insert(0, str(path.parent))
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    try:
        spec.loader.exec_module(module)
        return module
    finally:
        sys.path[:] = previous_path
        sys.modules.pop("_utils", None)
        if previous_utils is not None:
            sys.modules["_utils"] = previous_utils


class Chapter5ExampleTest(unittest.TestCase):
    def test_sharpening_examples_expose_independent_core_functions(self):
        expected = {
            "roberts_operator.py": "roberts_edges",
            "sobel_operator.py": "sobel_edges",
            "prewitt_operator.py": "prewitt_edges",
            "laplacian_operator.py": "laplacian_sharpen",
            "canny_edge_detection.py": "canny_edges",
            "log_filter.py": "log_edges",
        }
        folder = ROOT / "examples" / "05_image_sharpening"

        for filename, function_name in expected.items():
            with self.subTest(filename=filename):
                module = load_module(folder / filename)
                self.assertTrue(
                    callable(getattr(module, function_name, None)),
                    f"{filename} should define {function_name}()",
                )


class Chapter5CoverageToolTest(unittest.TestCase):
    def test_check_coverage_declares_chapter_5_requirements(self):
        module = load_module(ROOT / "tools" / "check_coverage.py")

        self.assertIn("5.1_图像细节的基本特征.md", module.REQUIRED_CHAPTER5_WIKI)
        self.assertIn("ch05_first_derivative_kernels.png", module.REQUIRED_CHAPTER5_FIGURES)
        self.assertIn("sobel_operator.py", module.REQUIRED_CHAPTER5_CODE)


if __name__ == "__main__":
    unittest.main()
