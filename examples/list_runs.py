from atlasmeta.ami.client import AMIClient
from atlasmeta.ami.query import get_runs
from atlasmeta.ami.auth import AMI_CONFIG, create_auth_config
import os

client = AMIClient()
if not os.path.exists(AMI_CONFIG):
    create_auth_config()
client.read_config(AMI_CONFIG)

runs = get_runs(client, periods=['B', 'K2'], year=11)
print runs
