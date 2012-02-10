.. -*- mode: rst -*-

For more information see `atlasmeta <http://cern.ch/noel.dawe/projects/atlasmeta>`_

About
-----

atlasmeta is a fork of `pyAMI <http://ccami01.in2p3.fr:8080/opencms/opencms/AMI/www/Tutorial/pyAMI.html>`_
with a cleaner codebase, enhanced API, and improved command-line functionality.
All commands are simply subcommands of ``ami``.

List AOD datasets matching a pattern::

   ami list datasets --type AOD data11_7TeV

list files in a dataset::

   ami list files -lhc dataset.name
   
list latest NTUP_TAUMEDIUM data datasets (and number of events in each one)
originating from AOD in periods I and J::

   ami list data --project data11_7TeV --type NTUP_TAUMEDIUM --parent-type AOD \
   --periods I,J --stream physics_JetTauEtmiss --latest --fields events %
   
list runs in a period or multiple periods::

   ami list runs B M

display dataset metadata::

   ami dataset info dataset.name

and query projects, data types, dataset provenance, etc.
``atlasmeta`` also provides an API allowing you to perform all of the same queries
from within your own Python program.

Requirements
------------

At least Python 2.6, `ZSI <http://pypi.python.org/pypi/ZSI/>`_, and `argparse <http://pypi.python.org/pypi/argparse>`_.
These packages and their dependencies are automatically downloaded and installed
by the ``setup.py`` script (mentioned below).


Install
-------

Get the latest tarball here: `http://cern.ch/noel.dawe/downloads/atlasmeta <http://cern.ch/noel.dawe/downloads/atlasmeta>`_

Untar and install (replace X appropriately)::

   tar -zxvf atlasmeta-X.tar.gz
   cd atlasmeta-X
   python setup.py install --user

Add ``${HOME}/.local/bin`` to your ``${PATH}`` if it is not there already (put this
in your .bashrc)::

   export PATH=${HOME}/.local/bin${PATH:+:$PATH}

Authenticate yourself::

   ami auth

This will prompt you for your AMI username and password.
You will only need to do this once since your credentials are stored in ~/.atlasmeta/ami.conf
for later use. If your credentials change just run ``ami auth`` again.
