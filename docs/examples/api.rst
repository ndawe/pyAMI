============
API Examples
============

A few examples of how to use pyAMI from our own Python application.

First create a client and authenticate:

.. testcode::

   from pyAMI.client import AMIClient
   from pyAMI.auth import AMI_CONFIG, create_auth_config
   import os
   
   client = AMIClient()
   if not os.path.exists(AMI_CONFIG):
      create_auth_config()
   client.read_config(AMI_CONFIG)

Query the runs contained by multiple data periods:

.. testcode::

   from pyAMI.query import get_runs
   
   runs = get_runs(client, periods=['B', 'K2'], year=11)

Query the cross section and generator efficiency for a dataset:

.. testcode::

   from pyAMI.query import get_dataset_xsec_effic
   
   dataset = 'mc11_7TeV.125206.PowHegPythia_VBFH130_tautauhh.evgen.EVNT.e893'
   xsec, effic = get_dataset_xsec_effic(client, dataset)
