
try:
   import setup_pyAMI # this line needed to ensure correct python environment since pyAMI 4.0.3
except Exception :
   print("Exception")
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

# SQL syntax - goes to a specific catalogue

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
      
argv=[]
argv.append("SearchQuery") 
#gLite syntax - searches over ALL catalogues  - can be slower
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
except Exception, msg:
   error = str(msg) 
   print error
