from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="get-params",
    version="0.1.1",
    description="A package to fetch function arguments from a Python module",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Tollef Emil Jørgensen",
    author_email="tollefj@gmail.com",
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)