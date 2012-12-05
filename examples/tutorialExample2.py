import setup_pyAMI
 # the above line needed to ensure correct python environment since pyAMI 4.0.3
from pyAMI import endpoint
from pyAMI.client import AMIClient
from pyAMI.endpoint import get_endpoint,get_XSL_URL
from pyAMI.auth import AMI_CONFIG, create_auth_config
import os
# set up your arguments for your favourite command
argv=[]
argv.append("GetUserInfo")
# the following will fail on the replica but succeed on the main, because the replica is case sensitive!
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
