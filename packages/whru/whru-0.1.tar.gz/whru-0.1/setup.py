from setuptools import setup

setup(
    name='whru',
    version='0.1',
    description='My custom Python module',
    author='whr819987540',
    author_email='steeliron550@gmail.com',
    packages=['whru'],
    install_requires=[
        "torch",
        "tensorflow",
    ],
)