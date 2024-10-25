from setuptools import setup, find_packages

setup(
    name="ppm",
    version="0.1",
    packages=find_packages(where="ppm/src"),
    package_dir={"": "ppm/src"},
    entry_points={
        "console_scripts": [
            "ppm=main:main",  # Pointing directly to main.py
        ],
    },
)
