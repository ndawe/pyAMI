API Examples
============

A few examples of how to use pyAMI from your own Python application.


First create a client and authenticate:

.. testcode::

   import setup_pyAMI # this line was needed to ensure correct python environment since pyAMI 4.0.3. Since 4.1.1 it can be omitted
   from pyAMI.client import AMIClient
   from pyAMI.auth import AMI_CONFIG, create_auth_config
   import os
   
   client = AMIClient()
   if not os.path.exists(AMI_CONFIG):
      create_auth_config()
   client.read_config(AMI_CONFIG)

.. testoutput::
   :hide:
   :options: -ELLIPSIS, +NORMALIZE_WHITESPACE



You can use pyAMI to run commands from inside your own python programs.
Query the runs contained by multiple data periods:

.. testcode::
   
   from pyAMI.query import get_runs
   # This is the equivalent of ami list runs --year 11 B K2
   
   runs = get_runs(client, periods=['B', 'K2'], year=11)
   print runs
   
.. testoutput::
   :hide:
   :options: -ELLIPSIS, +NORMALIZE_WHITESPACE
   


Query the cross section and generator efficiency for a dataset:

.. testcode::

   import setup_pyAMI # this line was needed to ensure correct python environment since pyAMI 4.0.3. Since 4.1.1 it can be omitted. 
   from pyAMI.query import get_dataset_xsec_effic
   from pyAMI.client import AMIClient
   client = AMIClient()
   dataset = 'mc11_7TeV.125206.PowHegPythia_VBFH130_tautauhh.evgen.EVNT.e893'
   xsec, effic = get_dataset_xsec_effic(client, dataset)
   print (str(xsec))
   


Constructing an Arbitrary AMI Query
-----------------------------------
In this section we show how to send a command directly to the server.

The command and the command arguments are passed to the pyAMI client in a list.
The first member must be the name of the command.
Here is a complete example which performs an SQL query:

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
   # We are going to send the command "SearchQuery" to the server
   argv.append("SearchQuery") 
   
   # We use SQL syntax -  to query a specific catalogue

   argv.append(
      "-sql=select logicalDatasetName from dataset where "
      "dataType='AOD' and version like '%r3542' and datasetNumber=146932") 
         
   # Tell AMI in which catalogue you want to look. (Or use the gLite syntax - see below)
   argv.append('project=mc12_001')
   argv.append('processingStep=production')

   amiClient = AMIClient()

   try:
      result=amiClient.execute(argv)
      
      # Change the output format to csv. See the general AMI help for a list of available transforms
      
      print result.output('csv')
   except Exception, msg:
      error = str(msg) 
      print error
      
   argv=[]
   argv.append("SearchQuery") 
   #gLite syntax - searches over ALL AMI dataset catalogues  -  it can be slower
   argv.append(
      "-glite=select logicalDatasetName  where "
      "dataType='AOD' and version like '%r3542' and datasetNumber=146932")
      
    # tell AMI what is the main thing you are looking for. Notice that the table name is not included in the query
    # glite will work this out, and also if you ask for a field which is not in the dataset table, but is related to this table,
    # glite will construct the correct relational query.
    
   argv.append('entity=dataset')
    
   # Tells AMI to look in all dataset catalogues. 
   
   argv.append('project=Atlas_Production')
   argv.append('processingStep=Atlas_Production')

   amiClient = AMIClient()

   try:
      result=amiClient.execute(argv)
      
      # Change the output format to xml.
      
      print result.output('xml')
      # You can also get the raw DOM object - please consult the AMI team for an example.
   except Exception, msg:
      error = str(msg) 
      print error


 
Here is another example of sending a command directly to the server. It is the equivalent of the command line  `here <commands.html#sending-an-arbitrary-command-to-the-ami-server-a-tag-collector-example>`_

.. testcode::

   from pyAMI.client import AMIClient


   # set up your arguments for your favorite command
   # This is the equivalent of 
   # ami cmd TCGetPackageInfo fullPackageName="/External/pyAMI" processingStep="production" project="TagCollector"
   # \repositoryName="AtlasOfflineRepository"

   argv=[]
   # Remember the name of the command must be the first parameter
   argv.append("TCGetPackageInfo") 
   # The other parameters can be in any order

   argv.append("fullPackageName=/External/pyAMI")
   argv.append("repositoryName=AtlasOfflineRepository")
   # Tell AMI in which catalogue you want to look. TagCollector in this case.
   argv.append('project=TagCollector')
   argv.append('processingStep=production')

   amiClient = AMIClient()

   try:
      result=amiClient.execute(argv)
      # Other formats are xml, csv, html 
      # print.result.output('xml')
      #
      # or you can parse the DOM yourself.
      # rowsets = result.dom.getElementsByTagName('rowset')
      # etc.
   
      print result.output()
   except Exception, msg:
      error = str(msg) 
      print error
      

      




Switching Between Servers
-------------------------

Here is a complete example. In general the Main server at Lyon is faster, but
you can include a failover to the CERN replica if you wish. This example starts
with the replica end point, and a command known to fail.

.. testcode::

   import setup_pyAMI # this line needed to ensure correct python environment since pyAMI 4.0.3
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
        

