import sys

from setuptools import find_namespace_packages, setup

if sys.version_info < (3, 10):
    print("Error: Commons requires at least Python 3.10")
    print("Error: Please upgrade your Python version to 3.10 or later")
    sys.exit(1)

package_name = "dataos_calculator"
package_version = "0.0.1"
description = "Calculator Package"

requires = []
# TODO Fix the params
setup(
    name=package_name,
    version=package_version,
    install_requires=requires,
    packages=find_namespace_packages(include=["dataos_calculator*"]),
)