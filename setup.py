#!/usr/bin/env python

import os

kw = {}
use_distribute = False
if os.getenv('PYAMI_USE_DISTRIBUTE') in ('1', 'true'):
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
    packages = ['pyAMI']
    if sys.version_info >= (2, 5):
        kw['requires'] = ['ZSI', 'argparse', 'lxml']

from distutils.command.install_data import install_data
from glob import glob


execfile('pyAMI/info.py')


class install_pyami_data(install_data):

    def run(self):

        open('version.txt', 'w').write(VERSION)
        install_data.run(self)


setup(name='pyAMI',
      version=VERSION,
      description='The ATLAS Metadata Interface',
      long_description=open('README.rst').read(),
      author='The AMI Team',
      author_email=AUTHOR_EMAIL,
      url=URL,
      download_url=DOWNLOAD_URL,
      packages=packages,
      scripts=glob('scripts/*'),
      data_files=[('etc/pyAMI', ['version.txt'])],
      cmdclass={'install_data': install_pyami_data},
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
