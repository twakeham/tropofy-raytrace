from tropofy.app import Parameter, ParameterGroup


class RangeValidator(object):

    def __init__(self, min_value=0, max_value=0):
        self.min = min_value
        self.max = max_value

    def __call__(self, value):
        return self.min < value < self.max


class CameraParameters(ParameterGroup):
    x = Parameter(name="x", label="X", default=0.0, allowed_type=float)
    y = Parameter(name="y", label="Y", default=0.0, allowed_type=float)
    z = Parameter(name="z", label="Z", default=-0.5, allowed_type=float)
    depth = Parameter(name="depth", label="Recursive reflection depth", default=4, allowed_type=int, validator=RangeValidator(0, 6))


class ImageParameters(ParameterGroup):
    filename = Parameter(name="filename", label="Filename", default="render.png", allowed_type=str)
    width = Parameter(name="width", label="Width", default=400, allowed_type=int, validator=RangeValidator(1, 600))
    height = Parameter(name="height", label="Height", default=300, allowed_type=int, validator=RangeValidator(1, 600))