from setuptools import setup, find_packages

setup(
    name='kmlgeom',
    version='0.1',
    description='Get geometry from KML file',
    author='Jonas Solvsteen',
    author_email='josl@dhigroup.com',
    url='https://www.dhi-gras.com',
    packages=find_packages(),
    install_requires=['lxml'])
