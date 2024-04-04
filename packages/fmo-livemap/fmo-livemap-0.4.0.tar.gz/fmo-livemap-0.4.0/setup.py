import os
from setuptools import setup, find_packages

# read the contents of your README file
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

VERSION = os.getenv("CI_COMMIT_TAG", "0.0.0")

setup(
    name="fmo-livemap",
    version=VERSION,
    author="Gudjon Magnusson",
    author_email="gmagnusson@fraunhofer.org",
    description="Simple way to draw a line on a map in real-time",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=["livemap"],
    package_data={"": ["templates/*", "static/*"]},
    include_package_data=True,
    keywords=["Map", "real-time"],
    python_requires=">=3.7, <4",
    install_requires=[
        "flask>=2.0.0",
        "click>=8.0.0",
        "Flask-SocketIO>=5.3.0",
        "requests>=2.28.2",
        "geojson >= 3.1.0",
    ],
    entry_points={
        "console_scripts": [
            "livemap=livemap.cli:cli",
        ]
    },
)
