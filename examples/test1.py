
from pyAMI.client import AMIClient
from pyAMI.auth import AMI_CONFIG, create_auth_config
import os
   
client = AMIClient()
if not os.path.exists(AMI_CONFIG):
   create_auth_config()
client.read_config(AMI_CONFIG)
