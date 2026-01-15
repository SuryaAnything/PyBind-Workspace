import sys
import os
import unittest

# 1. Setup Path to find the Engine
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(os.path.join(project_root, "Engines"))

class TestGeometry(unittest.TestCase):
    def setUp(self):
        try:
            # Import the SINGLE library that contains classes from MULTIPLE files
            import ws_geometry_type1
            self.module = ws_geometry_type1
        except ImportError:
            self.fail("Could not import 'ws_geometry_type1'. Build failed or library name mismatch.")

    def test_point_rect_merge(self):
        """Test classes from File 1 (Geometry.cpp)"""
        print("\n>>> Testing File 1: Point & Rect")
        
        # Test Point
        p = self.module.Point()
        # We can't verify 'move' return value as it's void, but calling it verifies binding exists
        p.move(10, 20) 
        print("    [Success] Point.move() called")

        # Test Rect (Static)
        msg = self.module.Rect.print()
        self.assertEqual(msg, "Rect Class")
        print(f"    [Success] Rect.print() returned: {msg}")

        # Test Rect (Instance)
        r = self.module.Rect()
        # Note: Since C++ implementation was just declaration in your example, 
        # this might return garbage if not implemented, but the binding check is what matters.
        # Ensure your C++ implementation actually returns something if you check values!

    def test_circle_merge(self):
        """Test classes from File 2 (MoreGeometry.cpp)"""
        print("\n>>> Testing File 2: Circle")
        
        c = self.module.Circle()
        # c.get_circumference()
        print("    [Success] Circle class found in the same module!")

if __name__ == '__main__':
    unittest.main()