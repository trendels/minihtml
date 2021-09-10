import os
import re
from setuptools import setup, find_packages

with open(os.path.join("src", "minihtml", "__init__.py")) as f:
    VERSION = re.findall(r'^__version__ = "(.*)"', f.read(), re.MULTILINE)[0]

with open("README.md") as f:
    README = f.read()

setup(
    name="minihtml",
    version=VERSION,
    author="Stanis Trendelenburg",
    author_email="stanis.trendelenburg@gmail.com",
    url="https://github.com/trendels/minihtml",
    license="MIT",
    description="Simple HTML generation",
    long_description=README,
    long_description_content_type="text/markdown",
    classifiers = [
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Typing :: Typed",
    ],
    packages=find_packages("src"),
    package_dir={"": "src"},
    include_package_data=True,
    zip_safe=False,
)
