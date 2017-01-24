import unittest

from ..mathlib import Vector


class VectorTest(unittest.TestCase):

    def test_addition(self):
        a = Vector(2, 2, 2)
        b = Vector(1, 1, 1)
        c = a + b
        self.assertTrue(c.data.all(0) and c.data[0] == 3)

    def test_subtraction(self):
        a = Vector(2, 2, 2)
        b = Vector(1, 1, 1)
        c = a - b
        self.assertTrue(c.data.all(0) and c.data[0] == 1)

    def test_scalar_multiplication(self):
        a = Vector(1, 1, 1)
        b = a * 3
        self.assertTrue(b.data.all(0) and b.data[0] == 3)

    def test_magnitude(self):
        a = Vector(1, 0, 0)
        b = Vector(3, 0, 4)
        self.assertTrue(a.magnitude == 1)
        self.assertTrue(b.magnitude == 5)

    def test_normal(self):
        a = Vector(1, 0, 0).normal
        self.assertTrue(a.data[0] == 1 and a.data[1] == a.data[2] == 0)
        b = Vector(3, 0, 4).normal
        self.assertAlmostEqual(b.data[0], 3.0 / 5)
        self.assertEqual(b.data[1], 0)
        self.assertAlmostEqual(b.data[2], 4.0 / 5)

    def test_dot(self):
        a = Vector(1, 0, 0)
        b = Vector(0, 1, 0)
        self.assertTrue(a.dot(b) == 0)

