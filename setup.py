# setup file in order to create a python applicaiton pacakge using setuptools
from setuptools import setup, find_packages

setup(
    # module name
    name='rgrHelper',
    version='1.0',
    description='Radio Grid Run helper tools',
    licence='CCC BY-SA 4.0',
    author='Frédéric Noyer',
    author_email='info@radiogrid.run',
    py_modules=['rgr_helper'],
    install_requires=[
        'Click==8.1.3',
        'Jinja2==3.1.2',
        'Configparser==5.3.0',
        'datetime==5.1',
        'python-dotenv==1.0.0',
        'pytest==7.3.1',
        'what3words==3.1.1',
        'area==1.1.1',
        'geojson==3.0.0'
    ],
    entry_points='''
        [console_scripts]
        rgrHelper=rgr_helper:cli
    ''',
    package=find_packages('rgrHelper'),
    package_dir={'': 'rgrHelper'},
package_data={'': ['rgrHelper/conf/*.ini','rgrHelper/conf/*.j2']}
)
