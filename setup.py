#===============================================================================
# setup.py
#===============================================================================

"""Install the project"""




# Imports ======================================================================

from setuptools import find_packages, setup




# Setup ========================================================================

setup(
    name='ucsd-bisb-unofficial',
    version='0.0.25',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=['flask']
)

