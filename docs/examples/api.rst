API Examples
============

A few examples of how to use pyAMI from your own Python application.

First create a client and authenticate:

.. testcode::

   from pyAMI.client import AMIClient
   from pyAMI.auth import AMI_CONFIG, create_auth_config
   import os
   
   client = AMIClient()
   if not os.path.exists(AMI_CONFIG):
      create_auth_config()
   client.read_config(AMI_CONFIG)

You can use pyAMI to run commands from inside your own python programs.
Query the runs contained by multiple data periods:

.. testcode::

   from pyAMI.query import get_runs
   # This is the equivalent of ami list runs --year 11 B K2
   
   runs = get_runs(client, periods=['B', 'K2'], year=11)
   print runs

Query the cross section and generator efficiency for a dataset:

.. testcode::

   from pyAMI.query import get_dataset_xsec_effic
   
   dataset = 'mc11_7TeV.125206.PowHegPythia_VBFH130_tautauhh.evgen.EVNT.e893'
   xsec, effic = get_dataset_xsec_effic(client, dataset)
   

Constructing an Arbitrary AMI Query
-----------------------------------

The command and the command arguments are passed to the pyAMI client in a list.
The first member must be the name of the command.
Here is a complete example:

.. testcode::

   from pyAMI.client import AMIClient
   from pyAMI.endpoint import get_endpoint,get_XSL_URL
   from pyAMI.auth import AMI_CONFIG, create_auth_config

   import os

   # set up your arguments for your favorite command
   # This is the equivalent of 
   # ami cmd SearchQuery -sql="select logicalDatasetName from dataset where \
   # dataType='AOD' and version like '%r3542' and datasetNumber=146932" \
   # -project=mc12_001 -processingStep=production
   argv=[]
   argv.append("SearchQuery") 

   argv.append(
      "-sql=select logicalDatasetName from dataset where "
      "dataType='AOD' and version like '%r3542' and datasetNumber=146932")    
   # Tell AMI in which catalogue you want to look. (Or use the gLite syntax)
   argv.append('project=mc12_001')
   argv.append('processingStep=production')

   amiClient = AMIClient()

   try:
      result=amiClient.execute(argv)
      # Change the output format to csv.
      print result.output('csv')
   except Exception, msg:
      error = str(msg) 
      print error


Switching Between Servers
-------------------------

Here is a complete example. In general the Main server at Lyon is faster, but
you can include a failover to the CERN replica if you wish. This example starts
with the replica end point, and a command known to fail.

.. testcode::

   from pyAMI import endpoint
   from pyAMI.client import AMIClient
   from pyAMI.endpoint import get_endpoint,get_XSL_URL
   from pyAMI.auth import AMI_CONFIG, create_auth_config
   import os

   # set up your arguments for your favourite command

   argv=[]
   argv.append("GetUserInfo") 
   # the following will fail on the replica but succeed on the main,
   # because the replica is case sensitive!
   argv.append("amiLogin=ALBRAND")    
   #to use the replica 
   endpoint.TYPE = 'replica'

   print get_endpoint() 
   print get_XSL_URL()

   amiClient = AMIClient()
   # Read the config file of username and password. 
   # prompt if it is not there
   if not os.path.exists(AMI_CONFIG):
      create_auth_config()
   
   amiClient.read_config(AMI_CONFIG)

   try:
      result=amiClient.execute(argv)
      print "Reading from the CERN replica: "+result.output("xml")
   except Exception, msg:
      error = str(msg) 
      print error
      endpoint.TYPE = 'main'
      try:
         result=amiClient.execute(argv)
         print "Reading from the main server: "+result.output("xml")
      except Exception, msg:
         error = str(msg) 
         print error

