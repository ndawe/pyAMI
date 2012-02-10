#!/usr/bin/env python

from distribute_setup import use_setuptools
use_setuptools()

from setuptools import setup, find_packages
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
      packages=find_packages(),
      install_requires = ['python>=2.6', 'ZSI', 'argparse'],
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
      ]
     )
