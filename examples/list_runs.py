from pyAMI.client import AMIClient
from pyAMI.query import get_runs
from pyAMI.auth import AMI_CONFIG, create_auth_config
import os

client = AMIClient()
if not os.path.exists(AMI_CONFIG):
    create_auth_config()
client.read_config(AMI_CONFIG)

runs = get_runs(client, periods=['B', 'K2'], year=11)
print runs
