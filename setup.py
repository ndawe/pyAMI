#!/usr/bin/env python

import os
import sys
from glob import glob


requires = ['ZSI', 'argparse']

if os.getenv('PYAMI_NO_LXML') not in ('1', 'true'):
    requires.append('lxml')

kw = {}
if os.getenv('PYAMI_NO_DISTRIBUTE') in ('1', 'true'):
    from distutils.core import setup
    if sys.version_info >= (2, 5):
        kw['requires'] = requires
else:
    from distribute_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages
    kw['install_requires'] = requires

execfile('pyAMI/info.py')
open('version.txt', 'w').write(VERSION)

if os.getenv('PYAMI_AFS_INSTALL') in ('1', 'true'):
    prefix = '/afs/cern.ch/atlas/software/tools/atlasmeta/'
else:
    prefix = 'etc/pyAMI'

if 'install' in sys.argv:
    print __doc__

setup(name='pyAMI',
      version=VERSION,
      description='The ATLAS Metadata Interface',
      long_description=open('README.rst').read() + open('Changelog.rst').read(),
      author='The AMI Team',
      author_email=AUTHOR_EMAIL,
      url=URL,
      download_url=DOWNLOAD_URL,
      packages=['pyAMI'],
      scripts=glob('scripts/*'),
      data_files=[(prefix, ['version.txt'])],
      license='GPLv3',
      classifiers=[
        "Programming Language :: Python",
        "Topic :: Utilities",
        "Operating System :: POSIX :: Linux",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License (GPL)"
      ],
      **kw
     )

os.unlink('version.txt')
