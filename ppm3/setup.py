from setuptools import setup, find_packages

setup(
    name="ppm3",
    version="0.0.9",
    author="Rahul Das",
    author_email="rahulcodepython@gmail.com",
    description="A Python project manager.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/rahulcodepython/Python-Project-Manager.git",
    project_urls={
        "Bug Tracker": "https://github.com/rahulcodepython/Python-Project-Manager/issues",
        "Documentation": "https://github.com/rahulcodepython/Python-Project-Manager/blob/main/ppm3/README.md",
        "Source Code": "https://github.com/rahulcodepython/Python-Project-Manager",
    },
    packages=find_packages(),
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    keywords="ppm, project manager, python package, python project manager",
    python_requires=">=3.6",
    include_package_data=True,
    install_requires=[
        "inquirer == 3.4.0",
        "setuptools == 75.5.0",
        "colorama == 0.4.6",
    ],
    entry_points={
        "console_scripts": [
            "ppm=ppm3:main",
        ],
    },
)

# To build the package, run the following command:
# python setup.py sdist bdist_wheel
# To upload the package to PyPI, run the following command:
# twine upload dist/*
