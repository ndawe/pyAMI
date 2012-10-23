#!/usr/bin/env python

import os
import sys

# support calling setup.py from outside of the pyAMI dir
local_path = os.path.dirname(os.path.abspath(__file__))
# setup.py can be called from outside the rootpy directory
os.chdir(local_path)
sys.path.insert(0, local_path)

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

if use_lxml and os.getenv('PYAMI_NO_LXML') not in ('1', 'true'):
    requires.append('lxml')

kw = {}
if use_distribute and os.getenv('PYAMI_NO_DISTRIBUTE') not in ('1', 'true'):
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

if release:
    # write the version to pyAMI/info.py
    VERSION = open('version.txt', 'r').read().strip()
    import shutil
    shutil.move('pyAMI/info.py', 'info.tmp')
    trunk_info = ''.join(open('info.tmp', 'r').readlines())
    open('pyAMI/info.py', 'w').write(
            trunk_info.replace('trunk', VERSION))
    # write protected init
    shutil.move('pyAMI/__init__.py', 'init.tmp')
    prot_init = ''.join(open('etc/protected_init.py', 'r').readlines())
    open('pyAMI/__init__.py', 'w').write(
            prot_init.replace('{SYS_VERSION}', str(sys.version_info[:2])))

execfile('pyAMI/info.py')

if afs_install or os.getenv('PYAMI_AFS_INSTALL') in ('1', 'true'):
    kw['data_files'] = [
        ('/afs/cern.ch/atlas/software/tools/atlasmeta/',
            ['version.txt'])]

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
    license='GPLv3',
    packages=[
      'pyAMI',
      'pyAMI.backports',
      'pyAMI.tests',
    ],
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
    shutil.move('init.tmp', 'pyAMI/__init__.py')
