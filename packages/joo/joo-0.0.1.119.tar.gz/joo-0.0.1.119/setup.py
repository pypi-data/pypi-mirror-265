import os
from setuptools import setup, find_packages
import joo.sysutil as sysutil
import joo9.rmutil as rmutil

# get version information
version_filepath = "./lib/joo/__version__.py"
version = rmutil.get_version(version_filepath)

# get project description
readme_filepath = "./lib/joo/README.md"
long_description = sysutil.load_file_contents(readme_filepath)

# setup
setup(
    # version information
    name=version["name"],
    description=version["description"],
    version="{}.{}".format(version["version"], version["build"]),
    license=version["license"],
    author=version["author"],
    author_email=version["author_email"],
    url=version["url"],
    project_urls=version["project_urls"],

    # detailed information
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[],

    # package information
    package_dir={"": "lib"},
    packages=find_packages("lib"),
    include_package_data=True,

    # requirements
    platforms="any",
    python_requires="",
    setup_requires=[],
    install_requires=[]
)
