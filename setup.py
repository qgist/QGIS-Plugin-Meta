# -*- coding: utf-8 -*-

"""

QGIS Plugin Meta
Handling metadata from QGIS plugins
https://github.com/qgist/QGIS-Plugin-Meta

    setup.py: Used for package distribution

    Copyright (C) 2020 QGIST project <info@qgist.org>

<LICENSE_BLOCK>
The contents of this file are subject to the GNU General Public License
Version 2 ("GPL" or "License"). You may not use this file except in
compliance with the License. You may obtain a copy of the License at
https://www.gnu.org/licenses/old-licenses/gpl-2.0.txt
https://github.com/qgist/QGIS-Plugin-Meta/blob/master/LICENSE

Software distributed under the License is distributed on an "AS IS" basis,
WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License for the
specific language governing rights and limitations under the License.
</LICENSE_BLOCK>

"""


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# IMPORT
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

from setuptools import (
    find_packages,
    setup,
)
import os

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# SETUP
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# Package version
__version__ = "0.0.1"

# List all versions of Python which are supported
python_minor_min = 6
python_minor_max = 8
confirmed_python_versions = [
    "Programming Language :: Python :: 3.{MINOR:d}".format(MINOR=minor)
    for minor in range(python_minor_min, python_minor_max + 1)
]

# Fetch readme file
with open(os.path.join(os.path.dirname(__file__), "README.md")) as f:
    long_description = f.read()

# Define source directory (path)
SRC_DIR = "src"

# Install package
setup(
    name="qgspluginmeta",
    packages=find_packages(SRC_DIR),
    package_dir={"": SRC_DIR},
    version=__version__,
    description="Handling metadata from QGIS plugins",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="QGIST project",
    author_email="info@qgist.org",
    url="https://github.com/qgist/QGIS-Plugin-Meta",
    download_url="https://github.com/qgist/QGIS-Plugin-Meta/archive/v%s.tar.gz"
    % __version__,
    license="GPLv2",
    keywords=["gis", "qgis", "plugin", "plugins",],
    scripts=[],
    include_package_data=True,
    python_requires=">=3.{MINOR:d}".format(MINOR=python_minor_min),
    setup_requires=[],
    install_requires=["typeguard",],
    extras_require={
        "dev": [
            "black",
            "python-language-server[all]",
            "setuptools",
            "twine",
            "wheel",
        ]
    },
    zip_safe=False,
    entry_points={},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: MacOS X",
        "Environment :: Win32 (MS Windows)",
        "Environment :: X11 Applications",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: MacOS",
        "Operating System :: POSIX :: BSD",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: Implementation :: CPython",
    ]
    + confirmed_python_versions
    + [
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: GIS",
        "Topic :: Software Development :: Libraries",
    ],
)
