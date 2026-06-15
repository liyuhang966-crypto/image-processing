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


class Chapter8ExampleTest(unittest.TestCase):
    def test_color_examples_expose_independent_core_functions(self):
        expected = {
            "color_spaces.py": "convert_color_space",
            "white_balance.py": "white_balance",
            "gray_world.py": "gray_world_balance",
            "color_compensation.py": "color_compensation",
        }
        folder = ROOT / "examples" / "08_color_image_processing"

        for filename, function_name in expected.items():
            with self.subTest(filename=filename):
                module = load_module(folder / filename)
                self.assertTrue(
                    callable(getattr(module, function_name, None)),
                    f"{filename} should define {function_name}()",
                )


class Chapter8CoverageToolTest(unittest.TestCase):
    def test_check_coverage_declares_chapter_8_requirements(self):
        module = load_module(ROOT / "tools" / "check_coverage.py")

        self.assertIn("8.1_彩色的形成原理与基本概念.md", module.REQUIRED_CHAPTER8_WIKI)
        self.assertIn("ch08_color_spaces.png", module.REQUIRED_CHAPTER8_FIGURES)
        self.assertIn("white_balance.py", module.REQUIRED_CHAPTER8_CODE)


if __name__ == "__main__":
    unittest.main()
