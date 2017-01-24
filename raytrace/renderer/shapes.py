from abc import ABCMeta, abstractmethod

import numpy

from mathlib import Vector, Ray
from material import Material


class Shape(object):
    __metaclass__ = ABCMeta

    def __init__(self, material): # type: (Material) -> None
        self.material = material

    @abstractmethod
    def intersect(self, ray): # type: (Ray) -> float
        """
        Intersect ray with shape
        :param ray: Ray to try to intersect shape
        :return: float representing the distance from the origin of the ray to the intersection point
        """
        pass

    @abstractmethod
    def normal(self, position):  # type: (Vector) -> Vector
        """
        Get the normal at the Vector position
        :param position: Vector intersection point
        :return: surface normal Vector at position
        """
        pass


class Sphere(Shape):

    def __init__(self, x, y, z, radius, material): # type: (float, float, float, float, Material) -> None
        """
        Sphere shape initialiser
        :param x: x position of centre of sphere
        :param y: y position of centre of sphere
        :param z: z position of centre of sphere
        :param radius: radius of sphere
        :param material: Material to render the shape with
        """
        super(Sphere, self).__init__(material)
        self.centre = Vector(x, y, z)
        self.radius = radius

    def intersect(self, ray): # type: (Ray) -> float
        origin_to_centre = ray.origin - self.centre
        a = ray.direction.dot(ray.direction)
        b = 2 * ray.direction.dot(origin_to_centre)
        c = origin_to_centre.dot(origin_to_centre) - self.radius * self.radius

        discriminant = b * b - 4 * a * c
        # no real solutions - we didn't intersect the sphere
        if discriminant <= 0:
            return numpy.inf
        discriminantSqrt = numpy.sqrt(discriminant)

        q = (-b - discriminantSqrt) / 2.0 if b < 0 else (-b + discriminantSqrt) / 2.0
        t0 = q / a
        t1 = c / q
        t0, t1 = min(t0, t1), max(t0, t1)

        # return closest intersection that is in front of the camera
        if t1 >= 0:
            return t1 if t0 < 0 else t0

        return numpy.inf

    def normal(self, position): # type: (Vector) -> Vector
        return Vector(position.data - self.centre.data).normal


class Plane(Shape):

    def __init__(self, position, up, material): # type: (Vector, Vector, Material) -> None
        """
        Plane shape initialisation
        :param position: Vector of point on plane
        :param up: Vector of plane normal
        :param material: Material to render the shape with
        """
        super(Plane, self).__init__(material)
        self.position = position
        self.up = up

    def intersect(self, ray): # type: (Ray) -> float
        denominator = ray.direction.dot(self.up)
        if abs(denominator) < 0.0000001:
            return numpy.inf
        # vector division is icky
        facing = (self.position - ray.origin).dot(self.up) * (1 /  denominator)
        if facing < 0:
            return numpy.inf

        return facing

    def normal(self, position): # type: (Vector) -> Vector
        return self.up