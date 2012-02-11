# import pyAMI package
from pyAMI import *
try:
# instantiate an AMI client object
    amiclient=AMI(False)
    argv=[]
    # List releases 4

    argv.append("TCTagSummary")
    argv.append("output=csv")
    argv.append("project=TagCollector")
    argv.append("processingStep=production")
    #argv.append("onlyDiff=true") # show only tags lines where there are some differences
    #argv.append("noNA=true") # remove  lines where there is a non applicable tag version
    argv.append("releaseFilter=15.6.X.Y.Z-BTagging;TC:AtlasOffline:15.6.8;TC:AtlasProduction:15.6.8.6")
    argv.append("packageFilter=/Calorimeter/")

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
