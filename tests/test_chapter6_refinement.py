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


class Chapter6ExampleTest(unittest.TestCase):
    def test_segmentation_examples_expose_independent_core_functions(self):
        expected = {
            "threshold_segmentation.py": "threshold_segment",
            "max_entropy_threshold.py": "max_entropy_threshold",
            "otsu_threshold.py": "otsu_threshold",
            "region_growing.py": "region_growing_segment",
        }
        folder = ROOT / "examples" / "06_image_segmentation"

        for filename, function_name in expected.items():
            with self.subTest(filename=filename):
                module = load_module(folder / filename)
                self.assertTrue(
                    callable(getattr(module, function_name, None)),
                    f"{filename} should define {function_name}()",
                )


class Chapter6CoverageToolTest(unittest.TestCase):
    def test_check_coverage_declares_chapter_6_requirements(self):
        module = load_module(ROOT / "tools" / "check_coverage.py")

        self.assertIn("6.1_阈值分割方法.md", module.REQUIRED_CHAPTER6_WIKI)
        self.assertIn("ch06_threshold_histogram.png", module.REQUIRED_CHAPTER6_FIGURES)
        self.assertIn("region_growing.py", module.REQUIRED_CHAPTER6_CODE)


if __name__ == "__main__":
    unittest.main()
