import sys
import os
import unittest

# 1. Setup Path to find the compiled .so files
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(os.path.join(project_root, "Engines"))

# 2. Import the C++ Module
try:
    import integration_test
    print(f"✅ Loaded Module: {integration_test.__file__}")
except ImportError as e:
    print("❌ Failed to import 'integration_test'. Did you run ./run.sh --shared-lib?")
    print(f"   Error: {e}")
    sys.exit(1)

class TestIntegration(unittest.TestCase):
    
    def test_01_constructors_and_stl(self):
        """Test: Constructors and automatic std::vector conversion."""
        print("\n--- Test 01: Constructors & STL ---")
        
        # Default Constructor (buffer = {0.0, 0.0})
        node_default = integration_test.ComputeNode()
        self.assertAlmostEqual(node_default.get_average(), 0.0)
        print("  -> Default Constructor: OK")

        # Vector Constructor
        data = [10.0, 20.0, 30.0] # Python List
        node_custom = integration_test.ComputeNode(data) # Auto-converts to std::vector<float>
        self.assertAlmostEqual(node_custom.get_average(), 20.0) # (10+20+30)/3 = 20
        print(f"  -> Vector Constructor ([10, 20, 30]): Average={node_custom.get_average()} OK")

    def test_02_inheritance(self):
        """Test: Calling a method inherited from BaseSystem."""
        print("\n--- Test 02: Inheritance ---")
        
        node = integration_test.ComputeNode()
        
        # 'reset' is defined in BaseSystem, not ComputeNode.
        # If this call succeeds, Python knows ComputeNode IS-A BaseSystem.
        try:
            node.reset() 
            print("  -> Inherited method 'reset()' called successfully.")
        except AttributeError:
            self.fail("ComputeNode failed to inherit 'reset' from BaseSystem!")

    def test_03_overloading(self):
        """Test: Calling overloaded methods (process)."""
        print("\n--- Test 03: Overloading ---")
        
        # Init with [1.0, 1.0]
        node = integration_test.ComputeNode([1.0, 1.0])
        
        # Overload 1: process(float factor)
        node.process(5.0) # Buffer becomes [5.0, 5.0]
        self.assertAlmostEqual(node.get_average(), 5.0)
        print("  -> process(float): OK")

        # Overload 2: process(float factor, int iterations)
        # Multiply by 2.0, three times -> 5 * 2 * 2 * 2 = 40
        node.process(2.0, 3) 
        self.assertAlmostEqual(node.get_average(), 40.0)
        print("  -> process(float, int): OK")

    def test_04_operators(self):
        """Test: Operator Overloading (+) mapped to __add__."""
        print("\n--- Test 04: Operators ---")
        
        n1 = integration_test.ComputeNode([1.0, 2.0])
        n2 = integration_test.ComputeNode([10.0, 20.0])
        
        # This uses the C++ operator+
        n3 = n1 + n2 
        
        # Expected: [11.0, 22.0] -> Average 16.5
        avg = n3.get_average()
        self.assertAlmostEqual(avg, 16.5)
        print(f"  -> Operator+ result average: {avg} OK")

    def test_05_static_method(self):
        """Test: Static method call."""
        print("\n--- Test 05: Static Methods ---")
        
        ver = integration_test.ComputeNode.version()
        self.assertEqual(ver, "v1.0.4-alpha")
        print(f"  -> Static Version: {ver} OK")

if __name__ == '__main__':
    unittest.main()