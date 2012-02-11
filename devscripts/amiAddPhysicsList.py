import sys
from pyAMI import *

class amiAddPhysicsList:
    def __init__(self):
        return 
    def command(self , argv):
        argument = []
        argument.append("AddPhysicsList")
        argument.extend(argv)
        return argument


def main(argv):

    try:
        pyAMI_setEndPointType(argv)
        amiclient = AMI()
        result = amiclient.execute(amiAddPhysicsList().command(argv))     
        print result.output()

    except Exception, msg:   
        print msg

if __name__ == '__main__':
    main(sys.argv[1:])       


