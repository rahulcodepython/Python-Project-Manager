from setuptools import setup, find_packages
from ppm3.src.constraints import VERSION

# Read the long description from README.md


def read_long_description(file_path: str) -> str:
    """Read and return the content of the given file."""
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


# Package metadata
PACKAGE_NAME: str = "ppm3"
PACKAGE_VERSION: str = VERSION
AUTHOR: str = "Rahul Das"
AUTHOR_EMAIL: str = "rahulcodepython@gmail.com"
DESCRIPTION: str = "A Python project manager."
LONG_DESCRIPTION: str = read_long_description("README.md")
LONG_DESCRIPTION_CONTENT_TYPE: str = "text/markdown"
URL: str = "https://github.com/rahulcodepython/Python-Project-Manager.git"
PROJECT_URLS: dict = {
    "Bug Tracker": "https://github.com/rahulcodepython/Python-Project-Manager/issues",
    "Documentation": "https://github.com/rahulcodepython/Python-Project-Manager/blob/main/ppm3/README.md",
    "Source Code": "https://github.com/rahulcodepython/Python-Project-Manager",
}
CLASSIFIERS: list = [
    "Intended Audience :: Developers",
    "Programming Language :: Python :: 3",
    "Operating System :: OS Independent",
]
KEYWORDS: str = "ppm, project manager, python package, python project manager"
PYTHON_REQUIRES: str = ">=3.6"
INSTALL_REQUIRES: list = [
    "inquirer==3.4.0",
    "setuptools==78.1.0",
    "ruamel.yaml==0.18.10",
]
ENTRY_POINTS: dict = {
    "console_scripts": [
        "ppm=ppm3:main",
    ],
}

# Setup function
setup(
    name=PACKAGE_NAME,
    version=PACKAGE_VERSION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type=LONG_DESCRIPTION_CONTENT_TYPE,
    url=URL,
    project_urls=PROJECT_URLS,
    packages=find_packages(),
    classifiers=CLASSIFIERS,
    keywords=KEYWORDS,
    python_requires=PYTHON_REQUIRES,
    include_package_data=True,
    install_requires=INSTALL_REQUIRES,
    entry_points=ENTRY_POINTS,
)

# To build the package, run the following command:
# python setup.py sdist bdist_wheel
# To upload the package to PyPI, run the following command:
# twine upload dist/*
