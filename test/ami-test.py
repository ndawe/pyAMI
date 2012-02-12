#!/usr/bin/env python
'''
Created on 22 sept. 2010

@author: lambert
'''
import sys
from pyAMI import *

def main(argv):
    try:
        amiclient = AMIClient()
        #amiclient.auth(user, password)

        argv = []


        argv.append("FormUserValidation")

        #argv.append("GetUserInfo")
        #argv.append("output=xml")
        #argv.append("amiLogin=atlas")

        #execute the command
        result = amiclient.execute(argv)

        #print the default output of the command result
        # The default output=text, but others can be set using argument output.
        print 'Test xml/xsl -> txt\n'
        print result.output(fornat='text')

        #print 'Test xml -> dom -> dict\n'
        #print result.getDict();
        return 0
    except Exception, msg:
        print msg
        return 1
if __name__ == '__main__':
    main(sys.argv[1:])
