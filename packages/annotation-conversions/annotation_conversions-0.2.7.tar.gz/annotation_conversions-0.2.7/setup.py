import io
import os
import re

import setuptools


def get_version():
    current_dir = os.path.abspath(os.path.dirname(__file__))
    version_file = os.path.join(current_dir, "labelme2coco", "__init__.py")
    with io.open(version_file, encoding="utf-8") as f:
        return re.search(r'^__version__ = [\'"]([^\'"]*)[\'"]', f.read(), re.M).group(1)


setuptools.setup(
    name="annotation_conversions",
    version=get_version(),
    author="Ishan Nangia",
    author_email="ishannangia.123@gmail.com",
    description="Converts one annotation format to another in a single step",
    url="https://github.com/beatboxerish/labelme2coco",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['sahi>=0.8.19', 'jsonschema>=2.6.0'],
    python_requires=">=3.7",
    download_url="https://github.com/beatboxerish/labelme2coco/archive/refs/tags/v0.2.6.tar.gz",
    entry_points={
        "console_scripts": [
            "labelme2coco=labelme2coco.cli:app",
        ],
    },
)
