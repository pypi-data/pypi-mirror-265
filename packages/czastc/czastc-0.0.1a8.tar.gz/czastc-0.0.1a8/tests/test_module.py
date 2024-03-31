"""
Test script for czastc module.
"""
import unittest
import czastc
class TestModule(unittest.TestCase):
    """
    Test cases for the czastc module.
    """
    def test_greet(self):
        """
        Test the greet function.
        """
        self.assertEqual(czastc.greet("CZAsTc"), "Hello, CZAsTc!")
        self.assertEqual(czastc.greet("world"), "Hello, world!")
if __name__ == "__main__":
    unittest.main()
