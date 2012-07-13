# -*- coding: utf-8 -*-

from ez_setup import use_setuptools
use_setuptools()
from setuptools import setup, find_packages

long_desc = '''
This package contains the specdomain Sphinx extension.

''' + open('README').read()

version = open('VERSION').read().strip()

requires = ['Sphinx>=0.6']

# classifiers: http://pypi.python.org/pypi?%3Aaction=list_classifiers

setup(
    name='sphinxcontrib-specdomain',
    version=version,
    url='https://subversion.xray.aps.anl.gov/bcdaext/specdomain/trunk/src/specdomain/', 
    #'http://bitbucket.org/birkenfeld/sphinx-contrib',
    #download_url='http://pypi.python.org/pypi/sphinxcontrib-specdomain',
    license='Argonne OPEN SOURCE LICENSE, see LICENSE file for details',
    author='Pete Jemian',
    author_email='jemian@anl.gov',
    description='Sphinx "specdomain" extension',
    long_description=long_desc,
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: Free To Use But Restricted',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Documentation',
        'Topic :: Utilities',
    ],
    platforms='any',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requires,
    namespace_packages=['sphinxcontrib'],
)
