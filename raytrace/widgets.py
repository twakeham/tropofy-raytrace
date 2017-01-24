import os.path
import ftplib

from matplotlib.pyplot import imsave
from tropofy.widgets import StaticImage, ExecuteFunction
from tropofy.app import AppDataSet

import renderer
import models
from parameters import CameraParameters, ImageParameters


class OutputImage(StaticImage):
    def get_file_path(self, app_session):
        filename = app_session.data_set.get_param(ImageParameters.filename.name)
        return 'http://fs.tjwakeham.com/tropofy/' + filename


class ExecuteRender(ExecuteFunction):
    def get_button_text(self, app_session):
        return "Render"

    def execute_function(self, app_session):
        app_session.task_manager.send_progress_message('Generating scene')

        # set up scene objects
        camera = renderer.Camera(
            x=app_session.data_set.get_param(CameraParameters.x.name),
            y=app_session.data_set.get_param(CameraParameters.y.name),
            z=app_session.data_set.get_param(CameraParameters.z.name),
            ray_depth=app_session.data_set.get_param(CameraParameters.depth.name),
            width=app_session.data_set.get_param(ImageParameters.width.name),
            height=app_session.data_set.get_param(ImageParameters.height.name),
        )

        materials = {}
        for material in app_session.data_set.query(models.Material).all():
            materials[material.name] = renderer.Material(
                name=material.name,
                r=material.red,
                g=material.green,
                b=material.blue,
                reflectance=material.reflectance
            )

        shapes = []
        for sphere in app_session.data_set.query(models.Sphere).all():
            shapes.append(renderer.Sphere(
                x=sphere.x,
                y=sphere.y,
                z=sphere.z,
                radius=sphere.radius,
                material=materials[sphere.material]
            ))

        lights = []
        for light in app_session.data_set.query(models.Light).all():
            lights.append(renderer.Light(
                x=light.x,
                y=light.y,
                z=light.z,
                power=light.power
            ))

        # add in a floor
        white = renderer.Material('_white', 1.0, 1.0, 1.0, 0.9)
        shapes.append(renderer.Plane(renderer.Vector(0.0, -0.5, 0.0), renderer.Vector(0.0, 1.0, 0.0), white))

        scene = renderer.Scene(shapes, lights, camera)

        app_session.task_manager.send_progress_message('Rendering scene')

        filename = app_session.data_set.get_param(ImageParameters.filename.name)
        path = os.path.join('static', filename)

        raytracer = renderer.Raytracer(scene)
        image = raytracer.render(update_callback=app_session.task_manager.send_progress_message)
        imsave(path, image)

        app_session.task_manager.send_progress_message('Rendering complete!')

        app_session.task_manager.send_progress_message('Uploading image')

        # upload file to server
        try:
            session = ftplib.FTP('tjwakeham.com', 'tropofy', 'N0T@RealPW!')
            session.cwd('application')
            with open(path, 'rb') as img_file:
                session.storbinary('STOR {0}'.format(filename), img_file)
            session.close()
            app_session.task_manager.send_progress_message('Done!')
        except ftplib.all_errors:
            app_session.task_manager.send_progress_message('Failed to upload image, please try again')

