from typing import Callable, Optional
from random import random

import numpy

from mathlib import Vector, Ray, lerp
from scene import Scene


class Raytracer(object):

    def __init__(self, scene): # type: (Scene) -> None
        """
        Algorithmically generates an image from a scene description by tracing rays into the scene
        testing whether they hit any objects.
        :param scene: Scene object describing scene to be rendered
        """
        self.scene = scene

    def trace(self, ray): # type: (Ray) -> Vector
        """
        Traces a ray into the scene testing for intersections against shapes
        :param ray: Ray object to trace into scene
        :return: Vector colour at intersection point or background colour for no intersection
        """
        hit_object = None
        t = numpy.inf

        for scene_object in self.scene.shapes:
            t0 = scene_object.intersect(ray)
            if t0 < t:
                t = t0
                hit_object = scene_object

        # if there were no intersections, then return the background colour
        if t == numpy.inf:
            return self.scene.camera.background

        hit_point = ray.origin + ray.direction * t
        normal = hit_object.normal(hit_point)
        luminance = 0.0

        # perform shading calculations
        for light in self.scene.lights:
            hit_point_to_light = (light.centre - hit_point).normal

            #check whether this light contributes to the shading
            in_shadow = False
            for shadower in self.scene.shapes:
                # we don't want to test against itself
                if shadower == hit_object:
                    continue
                shadow_ray = Ray(hit_point + normal * 0.0001, hit_point_to_light)
                if shadower.intersect(shadow_ray) < numpy.inf:
                    in_shadow = True
                    break
            if in_shadow:
                continue

            # super simple lambertian lighting model
            luminance += hit_point_to_light.dot(normal) * light.power

        # calculate shaded colour - luminance may be over one if there are multiple light sources
        # normally this would be dealt with by HDR and tone mapping but is just clipped
        # in demo ray tracers
        object_colour = hit_object.material.colour * min(luminance, 1.0)

        # calculate reflection colour if material has reflectance
        if hit_object.material.reflectance != 0.0 and ray.depth != self.scene.camera.depth:
            reflected_direction = (ray.direction - normal * 2 * (ray.direction.dot(normal))).normal
            # we need to 'translate' the reflection vector away from the hitpoint otherwise
            # we risk intersecting the original hit point again which causes artifacts in the reflection
            reflected_ray = Ray(hit_point + reflected_direction * 0.0001, reflected_direction, ray.depth + 1)
            reflection_colour = self.trace(reflected_ray)

            # interpolate shaded colour and reflected colour based on reflectance
            return Vector(*[lerp(object_colour.data[i], reflection_colour.data[i], hit_object.material.reflectance) for i in range(3)])

        return object_colour

    def render(self, subsamples=0, update_callback=None): # type: (Optional[Callable]) -> numpy.ndarray
        """
        Raytrace the scene
        :param subsamples: Number of samples per pixel.  Significantly increases render times for large values
        :param update_callback: Callback to provide progress information to
        :return: numpy.ndarray of pixels
        """

        # make camera local so we're not doing millions of attribute look ups for no reason
        camera = self.scene.camera
        aspect = float(camera.width) / camera.height
        screen_space = (-1.0, -1.0 / aspect + 0.25, 1.0, 1.0 / aspect + 0.25)

        image = numpy.zeros((camera.height, camera.width, 3))

        # we need pixel size scaled to screen space for subsampling
        if subsamples:
            inv_subsample = 1.0 / subsamples
            screen_x = float(screen_space[2] - screen_space[0]) / camera.width * 2.0
            screen_y = float(screen_space[3] - screen_space[1]) / camera.height * 2.0

        for x_index, x in enumerate(numpy.linspace(screen_space[0], screen_space[2], camera.width)):
            if update_callback and x_index % 10 == 0:
                update_callback('{0}% complete'.format(100.0 * x_index / camera.width))

            for y_index, y in enumerate(numpy.linspace(screen_space[1], screen_space[3], camera.height)):
                # single sample per pixel through top left of pixel
                if subsamples == 0:
                    screen_coords = Vector(x, y, 0.0)
                    camera_to_screen = (camera.position - screen_coords).normal
                    ray = Ray(camera.position, camera_to_screen)
                    colour = self.trace(ray)

                # multiple samples per pixel averaged for antialiasing - requires at least 12 samples
                # to look decent - multiplies render time
                else:
                    colour = Vector(0.0, 0.0, 0.0)
                    for sample in range(subsamples):
                        screen_coords = Vector(x + random() * screen_x, y + random() * screen_y, 0.0)
                        camera_to_screen = (camera.position - screen_coords).normal
                        ray = Ray(camera.position, camera_to_screen)
                        colour = colour + self.trace(ray) * inv_subsample

                image[y_index, x_index, :] = numpy.clip(colour.data, 0, 1)

        return image