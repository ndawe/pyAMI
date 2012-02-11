# import pyAMI package
from pyAMI import *
try:
# instantiate an AMI client object
    amiclient=AMI(False)
    argv=[]
    # List releases 4

    argv.append("TCListRelease")
    argv.append("output=xml")
    argv.append("groupName=BTagging")
    argv.append("project=TagCollector")
    argv.append("processingStep=production")

    #execute the command
    result= amiclient.execute(argv)

    #print the default output of the command result
    # The default output=text, but others can be set using argument output.
    print result.output()

    # return a dictionary (of dictionaries of dictionaries )containing all rowsets in the result
    #resultDict=result.getDict()

    # write a GPickle file containing a dictionary of all rowsets in the result
    # file named 'test.gpickle'
    #result.writeGPickle('test.gpickle')

except Exception, msg:
    print msg
