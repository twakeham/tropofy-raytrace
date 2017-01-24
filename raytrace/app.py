from tropofy.app import AppWithDataSets, Step, StepGroup
from tropofy.widgets import SimpleGrid, ParameterForm

from raytrace.models import Material, Sphere, Light

from widgets import OutputImage, ExecuteRender
from parameters import CameraParameters, ImageParameters


class RaytracerApp(AppWithDataSets):

    def get_name(self):
        return "Raytracer"

    def get_parameters(self):
        return CameraParameters.get_params() + ImageParameters.get_params()

    def get_examples(self):
        return {'Demo scene': self.load_demo_scene_data}

    def load_demo_scene_data(self, app_session):
        materials = [
            Material(name="red", red=0.8, green=0.1, blue=0.1, reflectance=0.25),
            Material(name="green", red=0.5, green=0.9, blue=0.1, reflectance=0.25),
            Material(name="blue", red=0.1, green=0.4, blue=0.8, reflectance=0.25)
        ]
        app_session.data_set.add_all(materials)

        spheres = [
            Sphere(x=-0.5, y=0.0, z=-2.0, radius=0.75, material="red"),
            Sphere(x=1.0, y=0.0, z=-2.0, radius=0.5, material="blue"),
            Sphere(x=-0.5, y=-0.25, z=-1.25, radius=0.25, material="green")
        ]
        app_session.data_set.add_all(spheres)

        lights = [
            Light(x=0.0, y=2.0, z=-2.0, power=0.75),
            Light(x=0.0, y=0.5, z=-1.0, power=0.75)
        ]
        app_session.data_set.add_all(lights)


    def get_gui(self):
        return [
            StepGroup(
                name="Parameters",
                steps=[
                    Step(
                        name='Camera',
                        widgets=[
                            ParameterForm(
                                title='Position',
                                parameter_names_filter=[
                                    CameraParameters.x.name,
                                    CameraParameters.y.name,
                                    CameraParameters.z.name,
                                ]
                            ),
                            ParameterForm(
                                title="Rendering quality",
                                parameter_names_filter=[
                                    CameraParameters.depth.name
                                ]
                            )
                        ]
                    ),
                    Step(
                        name="Output",
                        widgets=[
                            ParameterForm(
                                title='Resolution',
                                parameter_names_filter=[
                                    ImageParameters.filename.name,
                                    ImageParameters.width.name,
                                    ImageParameters.height.name
                                ]
                            )
                        ]
                    )
                ]
            ),
            StepGroup(
                name="Scene",
                steps=[
                    Step(
                        name="Define materials",
                        widgets=[SimpleGrid(Material)]
                    ),
                    Step(
                        name="Define objects",
                        widgets=[SimpleGrid(Sphere)]
                    ),
                    Step(
                        name="Define lights",
                        widgets=[SimpleGrid(Light)]
                    )
                ]
            ),
            StepGroup(
                name="Render",
                steps=[
                    Step(
                        name="Run renderer",
                        widgets=[ExecuteRender()]
                    )
                ]
            ),
            StepGroup(
                name="View Output",
                steps=[
                    Step(
                        name="Image",
                        widgets=[OutputImage()]
                    )
                ]
            )
        ]
