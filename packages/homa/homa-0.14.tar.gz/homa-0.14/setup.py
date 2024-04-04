from setuptools import setup
from setuptools import find_packages
from sys import argv

with open("README.md") as fh:
    description = fh.read()

with open("version.txt", "r") as fh:
    current_version = float(fh.readline())

with open("version.txt", "w") as fh:
    next_version = current_version + 0.01
    fh.write(str(next_version))

setup(
    name="homa",
    maintainer="Taha Shieenavaz",
    maintainer_email="tahashieenavaz@gmail.com",
    version=round(next_version, 2),
    packages=find_packages(),
    install_requires=[
        "opencv-python",
        "numpy"
    ],
    long_description=description,
    long_description_content_type="text/markdown",
)
