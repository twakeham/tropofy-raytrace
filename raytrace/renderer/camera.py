from mathlib import Vector


class Camera(object):
    def __init__(self, x, y, z, ray_depth, width, height): # type: (float, float, float, int, int, int) -> None
        """
        Initialise camera
        :param x: x position in 3d space
        :param y: y position in 3d space
        :param z: z position in 3d space
        :param ray_depth: maximum depth to recursively follow rays
        :param width: width of output
        :param height: height of output
        """
        self.position = Vector(x, y, z)
        self.depth = ray_depth
        self.width = width
        self.height = height
        self.background = Vector(0.0, 0.0, 0.0)
