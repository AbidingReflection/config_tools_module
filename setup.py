from setuptools import setup, find_packages

setup(
    name='config_tools',
    version='0.1.0',
    description='A configuration loader and validator tool for Python projects',
    author='Jacob Dec',
    packages=find_packages(exclude=["tests*"]), 
    install_requires=[
        'PyYAML',
    ],
    python_requires='>=3.7', 
)
