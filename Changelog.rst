.. -*- mode: rst -*-


Version 4.1.0 (4/2/2013)
--------------------------

* A patched version of ZSI is now included in pyAMI.extern that removes
  dependency on PyXML.
* argparse is now included in pyAMI.extern.
* A minimal pyAMI installation (no lxml) now does not depend on any external
  non-standard library packages.
* Added the -F and --from-file to the "ami list datasets" command where the
  pattern is interpreted as a file name which will be read for patterns (one per
  line, ignoring blank lines or lines beginning with #).
* Added the option to perform literal matches with "ami list datasets"
  using the new optional flags -L or --literal-match. In this case the pattern
  is interpreted as a literal string and the results must match exactly.
  A literal match query is much faster than a patterned match and can greatly
  speed up commands where you want to query information for known elements.
  This option pairs nicely with the new --from-file feature mentioned above for
  files listing many complete dataset names that should be interpreted literally
  and not as patterns.
* AMI errors are now printed correctly.

Version 4.0.4 (6/11/2012)
--------------------------

* Fix globbing issue. Only surround pattern with % if the pattern didn't have %
  on both ends originally. (it needed more fixing!)
  
Version 4.0.3 (11/10/2012)
--------------------------

* Skip version 4.0.2 to sync with ATLAS SVN tag version
* Fix setup.py for py2.4 compatibility
* Make ami-status=VALID default
* Fix globbing issue. Only surround pattern with % if the pattern didn't have %
  on both ends originally.

Version 4.0.1 (20/9/2012)
-------------------------

* This is pyAMI-04-00-01 in the ATLAS release
* Minor syntax changes in the API
* Added Windows installation to the doc
* Expanded doc section on API

Version 4.0.0a3 (17/4/2012)
---------------------------

* Make distribute the default install method
* Include patched urllib2 module in pyAMI.backports

Version 4.0.0a2 (10/4/2012)
---------------------------

* Second prerelease of the new pyAMI
* Support for connection through a proxy (BNL)
* Other minor improvements 

Version 4.0.0a1 (28/3/2012)
---------------------------

* Prerelease of the new pyAMI
* Package renamed to pyAMI
* Speed improvements
* VOMS authentication
* Fixed permissions of ~/.pyami/ami.cfg
* Removed intermediate ami package
  Everything is now under pyAMI

atlasmeta versions below:

Version 0.4.0 (4/2/2012)
------------------------

* Now compatible with Python 2.4
* Install with distutils by default and make installation with distribute optional
* Improved parent-type feature in dataset query
* Ability to specify a good runs list (GRL) in 'ami list data' and only
  the runs contained in the GRL are shown
* Installed on LXPLUS at CERN
* XSL transformations reimplemented

Version 0.3.1 (10/1/2012)
-------------------------
	
* Fix bug in file listing where size/events is NULL in database

Version 0.3 (20/12/2011)
------------------------
	
* Add ability to query datasets by parent type with --parent-type option
* list files in dataset with 'ami list files' and optionally display total size
  and events
* new schema module replicating AMI schema
* query files, projects, subprojects, datatypes, subdatatypes, tags, nomenclatures,
  production steps

Version 0.2 (17/12/2011)
------------------------

* Query and display additional dataset fields (i.e. datatype, number of events)

Version 0.1 (1/12/2011)
-----------------------

* Forked pyAMI
* Major code rewrite
* better command-line interface
