from mathlib import Vector

class Material(object):
    _materials = {}

    @classmethod
    def get_or_create(cls, name, r, g, b, reflectance): # type: (str, float, float, float, float) -> Material
        return cls._materials.get(name, Material(name, r, g, b, reflectance))

    def __init__(self, name, r, g, b, reflectance): # type: (str, float, float, float, float) -> Material
        """
        Initialise material
        :param name: unique material name
        :param r: red colour component
        :param g: green colour component
        :param b: blue colour component
        :param reflectance: fraction of colour determined by reflections
        """
        self.colour = Vector(r, g, b)
        self.reflectance = reflectance

        Material._materials[name] = self
