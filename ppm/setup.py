# setup.py

from setuptools import setup, find_packages

setup(
    name="ppm",
    version="0.1",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "ppm=ppm.main:main",  # This should match your main function
        ],
    },
)
