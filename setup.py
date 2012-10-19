#!/usr/bin/env python

import os
import sys


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
    from setuptools import setup
    kw['install_requires'] = requires

execfile('pyAMI/info.py')
version_patched = False
if VERSION == 'trunk' and 'install' not in sys.argv:
    # write the version to pyAMI/info.py
    VERSION = open('version.txt', 'r').read().strip()
    import shutil
    shutil.move('pyAMI/info.py', 'info.tmp')
    trunk_info = ''.join(open('info.tmp', 'r').readlines())
    open('pyAMI/info.py', 'w').write(
            trunk_info.replace('trunk', VERSION))
    version_patched = True

if os.getenv('PYAMI_AFS_INSTALL') in ('1', 'true'):
    prefix = '/afs/cern.ch/atlas/software/tools/atlasmeta/'
else:
    prefix = 'etc/pyAMI'

if 'install' in sys.argv:
    print __doc__

setup(
    name='pyAMI',
    version=VERSION,
    description='The ATLAS Metadata Interface',
    long_description=open('README.rst').read() + open('Changelog.rst').read(),
    author='The AMI Team',
    author_email=AUTHOR_EMAIL,
    url=URL,
    download_url=DOWNLOAD_URL,
    packages=[
      'pyAMI',
      'pyAMI.backports',
      'pyAMI.tests',
    ],
    entry_points = {
        'console_scripts': [
            'ami = pyAMI.ami:ami',
        ],
    },
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

if version_patched:
    # revert pyAMI/info.py
    shutil.move('info.tmp', 'pyAMI/info.py')
