import re

from tropofy.app import Parameter, ParameterGroup


class RangeValidator(object):
    '''
    Validator ensures that supplied value is between min_value and max_value
    '''
    def __init__(self, min_value=0, max_value=0):
        self.min = min_value
        self.max = max_value

    def __call__(self, value):
        return self.min < value < self.max


def image_filename_validator(value):
    '''Validator ensures a safe filename only is provided'''
    if re.match('^[a-zA-Z0-0_\-]+\.png$', value):
        return True
    return False


class CameraParameters(ParameterGroup):
    x = Parameter(name="x", label="X", default=0.0, allowed_type=float)
    y = Parameter(name="y", label="Y", default=0.0, allowed_type=float)
    z = Parameter(name="z", label="Z", default=-0.5, allowed_type=float)
    depth = Parameter(name="depth", label="Recursive reflection depth", default=4, allowed_type=int, validator=RangeValidator(0, 6))


class ImageParameters(ParameterGroup):
    filename = Parameter(name="filename", label="Filename", default="render.png", allowed_type=str, validator=image_filename_validator)
    width = Parameter(name="width", label="Width", default=400, allowed_type=int, validator=RangeValidator(1, 600))
    height = Parameter(name="height", label="Height", default=300, allowed_type=int, validator=RangeValidator(1, 600))