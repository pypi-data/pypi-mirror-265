#!/usr/bin/env python

"""The setup script."""

from setuptools import find_packages, setup

with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read()

requirements = [
    "Click>=7.0",
]

test_requirements = []

setup(
    author="Jude Odionye",
    author_email="odionye.jude@outlook.com",
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    description="A Python Client for the Argus Engine",
    entry_points={
        "console_scripts": [
            "argus_python=argus_python.cli:main",
        ],
    },
    install_requires=requirements,
    license="BSD license",
    long_description=readme + "\n\n" + history,
    include_package_data=True,
    keywords="argus_python",
    name="argus_python",
    packages=find_packages(include=["argus_python", "argus_python.*"]),
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/jayjaychukwu/argus-python",
    version="0.1.0",
    zip_safe=False,
)
