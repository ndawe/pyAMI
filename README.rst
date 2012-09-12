.. -*- mode: rst -*-

For more information see the full
`pyAMI documentation <https://atlas-ami.cern.ch/AMI/pyAMI/>`_

About
-----

pyAMI-04 is a major upgrade of the AMI python client. The command line syntax
has been rationalized, with improved help functions. pyAMI is available the
ATLAS software release, on lxplus, and can be installed standalone on a laptop.

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


From CVMFS
----------

ADD INFO HERE


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

To upgrade an existing installation use the ``-U`` option in the ``pip``
or ``easy_install`` commands above.


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

Add ``${HOME}/.local/bin`` to your ``${PATH}`` if it is not there
already (put this in your .bashrc)::

   export PATH=${HOME}/.local/bin${PATH:+:$PATH}

If you are unable to satisfy the requirement on lxml (only used for XSL
transformations) then you may disable this dependency before installation with::

   export PYAMI_NO_LXML=1


Installation on Windows
-----------------------

1. Install python, for example
`Python 2.7.3 <http://www.python.org/getit/releases/2.7.3/>`_

2. Install `distribute <http://python-distribute.org/distribute_setup.py>`_
(for easy set up of dependences)
For 64 bit machines there may be problems,
see __ http://bugs.python.org/issue6792

3. Download `pip <http://pypi.python.org/packages/source/p/pip/pip-1.1.tar.gz>`_

4. Install pip. Open a "cmd" terminal in windows. Assuming that you installed pip
below Python::

   cd C:\Python27\pip-1.1</br>
   C:\Python27\python setup.py install

5. Install pyAMI. ``pip.exe`` should be in ``C:\Python27\Scripts``::
   
   cd C:\Python27\Scripts
   pip install pyAMI

6. Install lxml to enable XSLT. If you don't install lxml, pyAMI will still work,
but you will only be able to obtain XML output on the command line.
However if you only want to use the API of pyAMI you may skip this step.::

   easy_install --allow-hosts=lxml.de,*.python.org lxml==2.2.8

7. Now so that you can use pyAMI conveniently you must ajust your paths in the
Windows environnement. (if you do not know how to do this follow the instructions
here __ http://www.java.com/en/download/help/path.xml
Add to the path::

   PATH    C:\PYTHON27;C:\PYTHON27\Scripts

8. Lastly explain to Windows that a python script can be executed.
Add to the ``PATHEXT`` variable::
   
   PATHEXT .PY

9. Then change the name of the file ``ami``  in ``C:\Python27\Scripts`` to ``ami.py``
so that script ami.py can be executed just by typing ``ami``.

**N.B. If you are not administrator of your machine you will probably need to
create the PATHEXT variable in your windows user environnement.**


Authentication
--------------

VOMS authentication is supported::

   voms-proxy-init -voms atlas

The alternative option (if gLite is not available)
is to send your username and password along with each AMI command::

   ami auth

This will prompt you for your AMI username and password.
You will only need to do this once since your credentials are stored in
~/.pyami/ami.conf for later use. If your credentials change just
run ``ami auth`` again. If you would like to keep your pyAMI configuration
in a directory other than ~/.pyami then set the environment
variable PYAMI_CONFIG_DIR.
