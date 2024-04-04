# Copyright (c) Microsoft Corporation. All rights reserved.
# Highly Confidential Material
"""URL checker tool to validate the reqired URLs accessible for AP5GC orject which were added in Firewall rules added."""

from setuptools import find_packages, setup

# read the contents of your README file
from pathlib import Path

VERSION = "0.0.2"
PACKAGE_NAME = "pmec-url-checker"

this_directory = Path(__file__).parent
long_description = (this_directory / "README_pypi.md").read_text()

DEPENDENCY = [
    "requests>=2.31.0",
    "dnspython>=2.6.1",
    "pandas>=2.2.1",
]

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    packages=find_packages(),
    install_requires=DEPENDENCY,
    # url="<git repo url>", #project home page.
    license="Copyright (c) Microsoft Corporation. All rights reserved.",
    author="Sagar Bhatt",
    author_email="sagbhatt@microsoft.com",
    # download_url=<python Artifect url>
    description="URL checker tool for AP5GC.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires=">=3.9",
    platforms="any",
    entry_points={
        "console_scripts": [
            "pmec-url-checker = pmec_url_checker.main:main",
        ],
    },
)
