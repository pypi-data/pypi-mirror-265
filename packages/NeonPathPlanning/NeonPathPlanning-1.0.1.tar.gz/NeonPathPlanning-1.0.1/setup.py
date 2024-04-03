from setuptools import find_packages, setup

setup(
    name="NeonPathPlanning",
    packages=find_packages(),
    version="1.0.1",
    description="Collection of autonomous robot path planners",
    long_description_content_type='text/markdown',
    long_description=open('README.md').read(),
    author="Project-Neon",
    author_email="projectneon@gmail.com",
    license="GNU",
    install_requires=['numpy'],
)
