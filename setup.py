import os
from setuptools import setup

# Allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))
README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()

setup(
    name = 'Constellation-OrderBoard',
    version = '0.1',
    packages = ['constellation_orderboard'],
    include_package_data = True,
    license = 'ISC License',
    description = 'Constellation Suite - Order Management',
    long_description = README,
    url = 'https://github.com/ConstellationApps/',
    author = 'Constellation Dev',
    author_email = 'null@example.com',
    install_requires=[
        'constellation_base',
    ],
    classifiers =[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ISC License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content'
    ]
)
