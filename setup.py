# -*- coding: utf-8 -*-
from setuptools import setup


def _readme():
    import os

    here = os.path.dirname(os.path.abspath(__file__))
    return open(os.path.join(here, "README.md")).read()


setup(
    name="make-clean",
    version=__import__("make_clean", fromlist=["__version__"]).__version__,
    author="Tomohiro NAKAMURA",
    author_email="quickness.net@gmail.com",
    url="https://github.com/jptomo/make-clean.py",
    description="A Cleanup Utility",
    long_description=_readme(),
    long_description_content_type="text/markdown",
    py_modules=["make_clean"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
    ],
    license="MIT License",
    entry_points={"console_scripts": ["make-clean = make_clean:main"]},
    extras_require={
        "dev": ["setuptools", "pytest", "pytest-cov"],
        'dev:python_version>="3.6"': ["flake8", "black", "isort[pyproject]", "pylint"],
        "release": ["twine", "wheel"],
    },
)
