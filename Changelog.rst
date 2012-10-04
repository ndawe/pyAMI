.. -*- mode: rst -*-


Version 4.0.1 (9/20/2012)
-------------------------

* This is pyAMI-04-00-01 in the ATLAS release
* Minor syntax changes in the API
* Added Windows installation to the doc.
* Expanded doc section on API

Version 4.0.0a3 (4/17/2012)
---------------------------

* Make distribute the default install method
* Include patched urllib2 module in pyAMI.backports

Version 4.0.0a2 (4/10/2012)
---------------------------

* Second prerelease of the new pyAMI
* Support for connection through a proxy (BNL)
* Other minor improvements 

Version 4.0.0a1 (3/28/2012)
---------------------------

* Prerelease of the new pyAMI
* Package renamed to pyAMI
* Speed improvements
* VOMS authentication
* Fixed permissions of ~/.pyami/ami.cfg
* Removed intermediate ami package.
  Everything is now under pyAMI

atlasmeta versions below:

Version 0.4.0 (2/4/2012)
------------------------

* Now compatible with Python 2.4
* Install with distutils by default and make installation with distribute optional.
* Improved parent-type feature in dataset query
* Ability to specify a good runs list (GRL) in 'ami list data' and only
  the runs contained in the GRL are shown.
* Installed on LXPLUS at CERN
* XSL transformations reimplemented

Version 0.3.1 (1/10/2012)
-------------------------
	
* Fix bug in file listing where size/events is NULL in database

Version 0.3 (12/20/2011)
------------------------
	
* Add ability to query datasets by parent type with --parent-type option
* list files in dataset with 'ami list files' and optionally display total size
  and events
* new schema module replicating AMI schema
* query files, projects, subprojects, datatypes, subdatatypes, tags, nomenclatures,
  production steps

Version 0.2 (12/17/2011)
------------------------

* Query and display additional dataset fields (i.e. datatype, number of events)

Version 0.1 (12/1/2011)
-----------------------

* Forked pyAMI
* Major code rewrite
* better command-line interface