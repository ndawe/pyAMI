# import pyAMI package
from pyAMI import *
try:
# instantiate an AMI client object
    amiclient=AMI(False)
    argv=[]
    #List Package Version Sample 1.a and 2

    argv.append("TCSearchPackageVersion")
    #argv.append("output=csv")
    argv.append("output=xml")
    #argv.append("withDep") # optionnal
    argv.append("keyword=")# leave empty for all
    argv.append("groupName=BTagging")
    argv.append("releaseName=15.6.8.6.1")
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
