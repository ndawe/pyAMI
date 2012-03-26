from pyAMI.userdata import DATA_ROOT
from pyAMI.config import AMIConfig
from getpass import getpass
import base64
import os


AMI_CONFIG = os.path.join(DATA_ROOT, 'ami.cfg')

if os.path.isfile(AMI_CONFIG):
    # only allow user to read and write
    os.chmod(AMI_CONFIG, 0600)


def create_auth_config():

    config = AMIConfig()
    config.set('AMI', 'AMIUser', raw_input('Username: '))
    config.set('AMI', 'AMIPass', base64.b64encode(getpass()))
    f = open(AMI_CONFIG, 'w')
    config.write(f)
    f.close()
    # only allow user to read and write
    os.chmod(AMI_CONFIG, 0600)
