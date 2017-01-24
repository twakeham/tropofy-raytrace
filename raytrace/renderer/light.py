from mathlib import Vector


class Light(object):
    def __init__(self, x, y, z, power): # type: (float, float, float, float) -> None
        """
        Initialise light
        :param x: x position in 3d space
        :param y: y position in 3d space
        :param z: z position in 3d space
        :param power: the power of the light
        """
        self.centre = Vector(x, y, z)
        self.power = power
