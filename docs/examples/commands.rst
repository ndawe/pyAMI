================
Command Examples
================

pyAMI provides the command ``ami`` under which various subcommands may be issued:

.. command-output:: ami --help

Listing Datasets
----------------

Use the subcommands ``ami list datasets`` to list datasets matching certain criteria:

.. command-output:: ami list datasets --help

For example, to list all NTUP_TAUMEDIUM datasets under the project mc11_7TeV:

.. command-output:: ami list datasets --project mc11_7TeV --type NTUP_TAUMEDIUM %
   :ellipsis: 20

Also print out the number of events in each dataset:

.. command-output:: ami list datasets --fields events data11_7TeV
   :ellipsis: 20


Listing Data Periods
--------------------

Use the ``ami list periods`` subcommands to list the periods in a given year (defaults to current year)
at a specific detail level:

.. command-output:: ami list periods --help

For example:

.. command-output:: ami list periods

To list data periods in 2010:

.. command-output:: ami list periods --year 10

Listing Data Runs
-----------------

Use the ``ami list runs`` subcommand to list all runs contained in the specified period(s):

.. command-output:: ami list runs --help

For example, to list runs in period M of the current year's data:

.. command-output:: ami list runs M
   :ellipsis: 20

You may also specify multiple periods:

.. command-output:: ami list runs K1 K2
   :ellipsis: 20


Listing Data Datasets/Containers
--------------------------------

.. command-output:: ami list data --help

.. command-output:: ami list data --periods M1 --type NTUP_TAUMEDIUM --latest p741
   :ellipsis: 20

Also print out the number of events in each dataset:

.. command-output:: ami list data --fields events --latest
   :ellipsis: 20


Retrieving Dataset Provenance
-----------------------------

Use the ``ami dataset prov`` subcommands to display a dataset's provenance:

.. command-output:: ami dataset prov --help

For example:

.. command-output:: ami dataset prov mc11_7TeV.125367.PythiaWH125_tautauhh.merge.NTUP_TAUMEDIUM.e825_s1310_s1300_r2730_r2700_p787

To restrict output to a certain datatype:

.. command-output:: ami dataset prov --type EVNT mc11_7TeV.125367.PythiaWH125_tautauhh.merge.NTUP_TAUMEDIUM.e825_s1310_s1300_r2730_r2700_p787

Retrieving Dataset Metadata
---------------------------

Use the ``ami dataset info`` subcommands to display a dataset's metadata:

.. command-output:: ami dataset info --help

For example:

.. command-output:: ami dataset info mc11_7TeV.125367.PythiaWH125_tautauhh.merge.NTUP_TAUMEDIUM.e825_s1310_s1300_r2730_r2700_p787

Use the ``ami dataset evtinfo`` subcommands to display a dataset's event generator metadata:

.. command-output:: ami dataset evtinfo --help

For example:

.. command-output:: ami dataset evtinfo mc11_7TeV.125367.PythiaWH125_tautauhh.merge.NTUP_TAUMEDIUM.e825_s1310_s1300_r2730_r2700_p787
