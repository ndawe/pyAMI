.. -*- mode: rst -*-

For more information see the full `pyAMI documentation <http://cern.ch/noel.dawe/projects/pyAMI>`_

About
-----

This is a prerelease of the new and improved pyAMI 
(formerly known as atlasmeta, a fork of the
`original pyAMI <http://ccami01.in2p3.fr:8080/opencms/opencms/AMI/www/Tutorial/pyAMI.html>`_)
This new version offers a cleaner codebase, enhanced API, and improved command-line functionality.
All commands are simply subcommands of ``ami``.

List AOD datasets matching a pattern::

   ami list datasets --type AOD data11_7TeV

list files in a dataset::

   ami list files -lhc dataset.name
   
list latest NTUP_TAUMEDIUM data datasets (and number of events in each one)
originating from AOD in periods L1 and L2 that are contained in a good runs list
(GRL)::

   ami list data --project data11_7TeV --type NTUP_TAUMEDIUM --parent-type AOD \
   --periods L1,L2 --stream physics_JetTauEtmiss --latest --fields events \
   --grl mygrl.xml
   
list runs in a period or multiple periods::

   ami list runs B M

display dataset metadata::

   ami dataset info dataset.name

and query projects, data types, dataset provenance, etc.
``pyAMI`` also provides an API allowing you to perform all of the same queries
from within your own Python program.


On LXPLUS at CERN
-----------------

pyAMI is installed centrally on LXPLUS at CERN. To begin using pyAMI
simply::

    source /afs/cern.ch/atlas/software/tools/atlasmeta/setup.sh

then authenticate yourself if you haven't already (see below).


Requirements
------------

At least Python 2.4, `ZSI <http://pypi.python.org/pypi/ZSI/>`_,
and `argparse <http://pypi.python.org/pypi/argparse>`_.
`lxml <http://lxml.de/>`_ is optional but required for XSL transformations.


Automatic Installation
----------------------

Automatically install the latest version of pyAMI with
`pip <http://pypi.python.org/pypi/pip>`_::

    pip install --user pyAMI

or with ``easy_install``::

    easy_install --user pyAMI

Omit the ``--user`` for a system-wide installation (requires root privileges).
Add ``${HOME}/.local/bin`` to your ``${PATH}`` if using ``--user`` and if
it is not there already (put this in your .bashrc)::

   export PATH=${HOME}/.local/bin${PATH:+:$PATH}

To upgrade an existing installation use the ``-U`` option in the ``pip`` or ``easy_install`` commands above.

Manual Installation
-------------------

Get the latest tarball on `PyPI <http://pypi.python.org/pypi/pyAMI/>`_

Untar and install (replace X appropriately)::

   tar -zxvf pyAMI-X.tar.gz
   cd pyAMI-X

pyAMI uses distribute to install but you may revert to a basic
disutils install by setting the environment variable::

   export PYAMI_NO_DISTRIBUTE=1

One advantage of using distribute is that all dependencies are automatically
downloaded and installed for you. To install pyAMI into your home directory
if using at least Python 2.6::

   python setup.py install --user

or with older Python versions::

   python setup.py install --prefix=~/.local

Add ``${HOME}/.local/bin`` to your ``${PATH}`` if it is not there already (put this
in your .bashrc)::

   export PATH=${HOME}/.local/bin${PATH:+:$PATH}

If you are unable to satisfy the requirement on lxml (only used for XSL
transformations) then you may disable this dependency before installation with::

   export PYAMI_NO_LXML=1


Authentication
--------------

VOMS authentication is supported::

   voms-proxy-init -voms atlas

The alternative option (if gLite is not available)
is to send your username and password along with each AMI command::

   ami auth

This will prompt you for your AMI username and password.
You will only need to do this once since your credentials are stored in ~/.pyAMI/ami.conf
for later use. If your credentials change just run ``ami auth`` again.
