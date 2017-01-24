import unittest

import numpy

from ..mathlib import Vector, Ray
from ..shapes import Sphere


class IntersectionTests(unittest.TestCase):

    def test_ray_sphere_intersection(self):
        sphere = Sphere(0, 0, 2, 0.5, None)
        origin = Vector(0, 0, -10)
        direction = Vector(0, 0, 1)
        ray = Ray(origin, direction)

        t = sphere.intersect(ray)
        self.assertAlmostEqual(t, 11.5)
