import setup_pyAMI
 # the above line needed to ensure correct python environment since pyAMI 4.0.3
from pyAMI.client import AMIClient
from pyAMI.query import get_datasets, print_table
from pyAMI.auth import AMI_CONFIG, create_auth_config
import os
import sys

class test1:
   def main(argv):
      client = AMIClient()
      if not os.path.exists(AMI_CONFIG):
         create_auth_config()
      client.read_config(AMI_CONFIG)
      datasetNamePattern=argv[0] 
      
      res =  get_datasets(client,datasetNamePattern,fields='events,nfiles', flatten=True)
      print_table( res )           
      
   if __name__ == '__main__':
	main(sys.argv[1:])  
