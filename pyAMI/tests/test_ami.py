#!/usr/bin/env python

from pyAMI.client import AMIClient


def client_test():

    amiclient = AMIClient()
    #amiclient.auth(user, password)

    argv = ['FormUserValidation']

    #argv.append("GetUserInfo")
    #argv.append("output=xml")
    #argv.append("amiLogin=atlas")

    # execute the command
    result = amiclient.execute(argv)

    # print the default output of the command result
    print 'Test xml/xsl -> txt'
    print result.output('text')

if __name__ == '__main__':
    import nose
    nose.runmodule()
