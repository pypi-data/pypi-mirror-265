"""
Test script for czastc.turtle module.
"""
import unittest
import czastc.turtle
class TestModule(unittest.TestCase):
    """
    Test cases for the czastc module.
    """
    def test_generate_color_gradient(self):
        """
        Test the generate_color_gradient function.
        """
        self.assertEqual(czastc.turtle.generate_color_gradient(
            6, [[255, 255, 0], [255, 0, 0], [255, 0, 255]]),
            [(1.0, 1.0, 0.0), (1.0, 0.5, 0.0), (1.0, 0.0, 0.0),
                (1.0, 0.0, 0.0), (1.0, 0.0, 0.5), (1.0, 0.0, 1.0)])
if __name__ == "__main__":
    unittest.main()
