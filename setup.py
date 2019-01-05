#===============================================================================
# setup.py
#===============================================================================

"""Install the project"""




# Imports ======================================================================

from setuptools import find_packages, setup




# Setup ========================================================================

setup(
    name='ucsd-bisb-unofficial',
    version='0.2.27',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'alembic',
        'atomicwrites',
        'attrs',
        'blinker',
        'click',
        'coverage',
        'flask',
        'flask-ftscursor',
        'flask-login',
        'flask-mail',
        'flask-migrate',
        'flask-misaka',
        'flask-principal',
        'flask-sqlalchemy',
        'flask-uploads',
        'flask-wtf',
        'itsdangerous',
        'jinja2',
        'mako',
        'markupsafe',
        'more-itertools',
        'pluggy',
        'py',
        'pyjwt',
        'python-dateutil',
        'python-editor',
        'six',
        'sqlalchemy',
        'werkzeug',
        'wtforms'
    ]
)

