from setuptools import setup, find_packages

setup(
    name='asynchronyClassifier',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'matplotlib',
        # Any other dependencies your library may have
    ],
    python_requires='>=3.6',
)