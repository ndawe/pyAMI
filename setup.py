#!/usr/bin/env python

import os
import sys

# check for custom args
# we should instead extend distutils...
use_lxml = True
use_distribute = True
afs_install = False
release = False
filtered_args = []
for arg in sys.argv:
    if arg == '--no-lxml':
        use_lxml = False
    elif arg == '--no-distribute':
        use_distribute = False
    elif arg == '--release':
        release = True
    elif arg == '--afs-install':
        afs_install = True
    else:
        filtered_args.append(arg)
sys.argv = filtered_args

requires = ['ZSI', 'argparse']

if use_lxml:
    requires.append('lxml')

kw = {}
if use_distribute:
    from distribute_setup import use_setuptools
    use_setuptools()
    from setuptools import setup
    kw['install_requires'] = requires
    kw['entry_points'] = {
        'console_scripts': [
            'ami = pyAMI.ami:ami',
        ],
    }
else:
    from distutils.core import setup
    if sys.version_info >= (2, 5):
        kw['requires'] = requires
    kw['scripts'] = ['scripts/ami']

execfile('pyAMI/info.py')
if release:
    # write the version to pyAMI/info.py
    VERSION = open('version.txt', 'r').read().strip()
    import shutil
    shutil.move('pyAMI/info.py', 'info.tmp')
    trunk_info = ''.join(open('info.tmp', 'r').readlines())
    open('pyAMI/info.py', 'w').write(
            trunk_info.replace('trunk', VERSION))

if afs_install:
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

if release:
    # revert pyAMI/info.py
    shutil.move('info.tmp', 'pyAMI/info.py')
