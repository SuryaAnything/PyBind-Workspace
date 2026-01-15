import sys
import os
import unittest

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(os.path.join(project_root, "Engines"))

class TestTurboEngine(unittest.TestCase):
    def setUp(self):
        # This will fail if the module wasn't built correctly
        try:
            import ws_engines
            self.module = ws_engines
        except ImportError:
            self.fail("Could not import 'ws_engines'. Did you run './run.sh --shared-lib'?")

    def test_hello(self):
        """Test the string return function"""
        result = self.module.say_hello()
        print(f"\n[C++] say_hello() returned: {result}")
        self.assertIsInstance(result, str)
        self.assertIn("Code-Driven", result)

    def test_add(self):
        """Test the integer addition function"""
        val_a = 10
        val_b = 25
        result = self.module.add_numbers(val_a, val_b)
        print(f"[C++] add_numbers({val_a}, {val_b}) returned: {result}")
        self.assertEqual(result, 35)

if __name__ == '__main__':
    unittest.main()