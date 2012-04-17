from fabric.api import *
from getpass import getpass

env.hosts = ['ftps://end.web.cern.ch']
env.user = raw_input('username: ')
env.password = getpass('password: ')


def upload_tarball(file):

    put(file, './e/end/downloads/pyAMI/')

