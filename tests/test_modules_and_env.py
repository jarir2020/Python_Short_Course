import unittest

from python_core.modules_and_env import explain_module_imports


class ModuleAndEnvTests(unittest.TestCase):
    """Unit tests for Lesson 5: Modules and Environments."""

    def test_explain_module_imports(self) -> None:
        info = explain_module_imports()
        self.assertIn("module", info)
        self.assertIn("package", info)
        self.assertIn("venv", info)
        self.assertIn("pip", info)


if __name__ == "__main__":
    unittest.main()
