#!/usr/bin/env python

import os
import sys
from glob import glob


requires = ['ZSI', 'argparse', 'lxml']
if sys.version_info < (2, 6):
    # http://pypi.python.org/pypi/httpsproxy_urllib2
    requires.append('httpsproxy_urllib2')

kw = {}
use_distribute = False
if os.getenv('PYAMI_USE_DISTRIBUTE') in ('1', 'true'):
    use_distribute = True
if use_distribute:
    from distribute_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages
    packages = find_packages()
    kw['install_requires'] = requires
else:
    from distutils.core import setup
    packages = ['pyAMI']
    if sys.version_info >= (2, 5):
        kw['requires'] = requires

execfile('pyAMI/info.py')
open('version.txt', 'w').write(VERSION)

if os.getenv('PYAMI_AFS_INSTALL') in ('1', 'true'):
    prefix = '/afs/cern.ch/atlas/software/tools/atlasmeta/'
else:
    prefix = 'etc/pyAMI'

print __doc__

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
      data_files=[(prefix, ['version.txt'])],
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

os.unlink('version.txt')
