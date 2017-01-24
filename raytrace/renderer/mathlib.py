from typing import Union

import numpy


def lerp(a, b, factor): # type: (float, float) -> float
    """
    Linear interpolation betweem two values
    :param a: first value
    :param b: second value
    :param factor: blending factor
    :return: interpolated value
    """
    return (1.0 - factor) * a + b * factor


class Vector(object):

    def __init__(self, x, y=0.0, z=0.0): # type: (Union[float, numpy.array], float, float) -> None
        """
        Vector initialisation
        :param x: float x component or numpy.ndarray[x, y, z]
        :param y: float y component
        :param z: float z component
        """
        if isinstance(x, numpy.ndarray):
            self.data = x
        else:
            self.data = numpy.array([x, y, z])

    def __add__(self, other): # type: (Vector) -> Vector
        return Vector(self.data + other.data)

    def __sub__(self, other): # type: (Vector) -> Vector
        return Vector(self.data - other.data)

    def __mul__(self, scalar): # type: (float) -> Vector
        return Vector(self.data * scalar)

    @property # type: float
    def magnitude(self):
        """
        Length of the vector
        :return: float length
        """
        return numpy.linalg.norm(self.data)

    @property # type: Vector
    def normal(self):
        """
        Normalised copy of vector - components are scaled such that the vector is a unit vector
        :return: normalised Vector
        """
        return Vector(self.data / self.magnitude)

    def dot(self, other): # type: (Vector) -> float
        """
        Take the dot product of two vectors
        :param other: other Vector
        :return: float dot product
        """
        return numpy.dot(self.data, other.data)


class Ray(object):

    def __init__(self, origin, direction, depth=0): # type: (Vector, Vector) -> None
        """
        Ray initialisation
        :param origin: position of start of ray
        :param direction: direction the ray points
        :param depth: optional depth count for use with recursive reflections
        """
        self.origin = origin
        self.direction = direction.normal
        self.depth = depth
