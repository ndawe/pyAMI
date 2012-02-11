#!/usr/bin/env python

import os

kw = {}
use_distribute = False
if os.getenv('ATLASMETA_USE_DISTRIBUTE') in ('1', 'true'):
    use_distribute = True
if use_distribute:
    from distribute_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages
    packages = find_packages()
    kw['install_requires'] = ['ZSI', 'argparse', 'lxml']
else:
    from distutils.core import setup
    import sys
    packages = ['atlasmeta',
                'atlasmeta/ami']
    if sys.version_info >= (2, 5):
        kw['requires'] = ['ZSI', 'argparse', 'lxml']

from glob import glob

execfile('atlasmeta/info.py')

setup(name='atlasmeta',
      version=__VERSION__,
      description='ATLAS metadata',
      long_description=open('README.rst').read(),
      author='Noel Dawe',
      author_email='noel.dawe@cern.ch',
      url=__URL__,
      download_url=__DOWNLOAD_URL__,
      packages=packages,
      scripts=glob('scripts/*'),
      license='GPLv3',
      classifiers=[
        "Programming Language :: Python",
        "Topic :: Utilities",
        "Operating System :: POSIX :: Linux",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License (GPL)"
      ],
      **kw
     )
