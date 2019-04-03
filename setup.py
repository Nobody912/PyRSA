import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PyRSA",
    python_requires='>3',
    version="1.0",
    author="Erik Ji",
    author_email="erikji@tuta.io",
    description="A simple implementation of PyCryptodome for RSA encryption in a CLI interface.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Nobody912/PyRSA",
    packages=setuptools.find_packages(),
    scripts=["scripts/pyrsa"],
    install_requires=[
        "termcolor",
        "pycryptodome",
        "halo",
        "pyfiglet",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
