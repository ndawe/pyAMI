try:
   import setup_pyAMI # this line needed to ensure correct python environment since pyAMI 4.0.3
except Exception :
   print("Exception")
from pyAMI.client import AMIClient
from pyAMI.auth import AMI_CONFIG, create_auth_config
import os
   
client = AMIClient()
if not os.path.exists(AMI_CONFIG):
   create_auth_config()
client.read_config(AMI_CONFIG)