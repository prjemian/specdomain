# -*- coding: utf-8 -*-

from ez_setup import use_setuptools
use_setuptools()
from setuptools import setup, find_packages

short_desc = 'Sphinx "specdomain" extension'
long_desc = short_desc + '\n'*2 + open('README').read()

version = open('VERSION').read().strip()

requires = ['Sphinx>=0.6']

# classifiers: http://pypi.python.org/pypi?%3Aaction=list_classifiers

setup(
    name='sphinxcontrib-specdomain',
    version=version,
    url='http://subversion.xray.aps.anl.gov/admin_bcdaext/specdomain', 
    #'http://bitbucket.org/birkenfeld/sphinx-contrib',
    #download_url='http://pypi.python.org/pypi/sphinxcontrib-specdomain',
    license='Argonne OPEN SOURCE LICENSE, see LICENSE file for details',
    author='Pete Jemian',
    author_email='jemian@anl.gov',
    description=short_desc,
    long_description=long_desc,
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Science/Research',
        'License :: Free To Use But Restricted',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Documentation',
        'Topic :: Utilities',
    ],
    platforms='any',
    packages=find_packages(exclude=['comparison', 'macros', 'test', 'doc', 'markup_example', ]),
    include_package_data=True,
    install_requires=requires,
    namespace_packages=['sphinxcontrib'],
)
