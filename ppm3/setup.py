from setuptools import setup, find_packages

setup(
    name="ppm3",
    version="0.0.3",
    author="Rahul Das",
    author_email="rahulcodepython@gmail.com",
    description="A Python package manager.",
    long_description="A Python package manager.",
    long_description_content_type="text/markdown",
    url="https://github.com/rahulcodepython/Python-Project-Manager.git",
    project_urls={
        "Bug Tracker": "https://github.com/rahulcodepython/Python-Project-Manager/issues",
        # "Documentation": "https://github.com/yourusername/your-repo-name#readme",
        "Source Code": "https://github.com/rahulcodepython/Python-Project-Manager",
    },
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    keywords="ppm, package manager, python package, python project manager",
    python_requires=">=3.6",
    include_package_data=True,
    install_requires=[
        "ansicon == 1.89.0",
        "blessed == 1.20.0",
        "editor == 1.6.6",
        "inquirer == 3.4.0",
        "jinxed == 1.3.0",
        "readchar == 4.2.0",
        "runs == 1.2.2",
        "setuptools == 75.3.0",
        "six == 1.16.0",
        "wcwidth == 0.2.13",
        "xmod == 1.8.1",
    ],
    entry_points={
        "console_scripts": [
            "ppm=ppm3:main",
        ],
    },
)

# To build the package, run the following command:
# python setup.py sdist bdist_wheel
