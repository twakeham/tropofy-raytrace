from typing import List

from mathlib import Vector
from shapes import Shape
from light import Light
from camera import Camera


class Scene(object):
    def __init__(self, shapes, lights, camera): # type: (List[Shape], List[Light], Camera) -> None
        """
        Scene initialisation
        :param shapes: list of Shape instances in the scene
        :param lights: list of Light instances in the scene
        :param camera: Camera instance defining the camera
        """
        self.shapes = shapes
        self.lights = lights
        self.camera = camera
