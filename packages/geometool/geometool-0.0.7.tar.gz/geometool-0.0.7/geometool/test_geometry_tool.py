import unittest
from math import pi
from geometry_tool import Circle, Triangle

class TestShapes(unittest.TestCase):

    def test_circle_area(self):
       circle = Circle(5)
       expected_area = pi * (5 ** 2)
       self.assertEqual(circle.calc_area(), expected_area)

    def test_triangle_area_rightangled(self):
       triangle = Triangle(6, 8, 9)
       expected_area = 23.525252389719434
       self.assertAlmostEqual(triangle.calc_area(), expected_area) 

    def test_triangle_is_rightangled(self):
        triangle_rightangled = Triangle(3, 4, 5)
        triangle_not_rightangled = Triangle(6, 7, 8)
        
        self.assertTrue(triangle_rightangled.is_rightangled())
        self.assertFalse(triangle_not_rightangled.is_rightangled())


if __name__ == '__main__':
   unittest.main()
