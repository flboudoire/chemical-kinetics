import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="chemical-kinetics",
    version="1.0.4",
    author="Florent Boudoire",
    author_email="flboudoire@gmail.com",
    description="Module to fit data with a chemical kinetics model.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/flboudoire/chemical-kinetics",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
