from setuptools import setup, find_packages

requires = [
    'tropofy',
]

setup(
    name='tropofy-raytrace',
    version='1.0',
    description='Demo Tropofy app',
    author='Tim Wakeham',
    url='http://blog.tjwakeham.com',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requires,
)
