'''
Created on 17 nov. 2010

@author: lambert
'''
# import pyAMI package
from pyAMI import *
try:
# instantiate an AMI client object

    groupName = "A Group Name"
    releaseName = "A Release Name.01"
    newReleaseName = ""
    isPatch = "yes"
    importApproval = "yes"

    project = "TagCollector"
    process = "production"



    #with login/password authentication
    amiclient = AMI(False)
    amiclient.auth("user", "password")

    #with grid proxy certificate
    #amiclient=AMI()


    if newReleaseName == "":
        tmpDigit = releaseName.split('.')
        i = 0
        while i < len(tmpDigit) - 1:
            newReleaseName = newReleaseName + tmpDigit[i] + "."
            i = i + 1

        newReleaseName = newReleaseName + "" + str(int(tmpDigit[i]) + 1)




    argv = []
    argv.append("TCAutoTagRelease")
    argv.append("groupName=" + groupName)
    argv.append("releaseName=" + releaseName)
    argv.append("project=" + project)
    argv.append("processingStep=" + process)
    #argv.append("output=xml")
    result = amiclient.execute(argv)
    print result.output()
    #print argv

    argv = []
    argv.append("TCTerminateRelease")
    argv.append("groupName=" + groupName)
    argv.append("releaseName=" + releaseName)
    argv.append("project=" + project)
    argv.append("processingStep=" + process)
    #argv.append("output=xml")
    result = amiclient.execute(argv)
    print result.output()
    #print argv


    argv = []
    argv.append("TCCreateRelease")
    argv.append("groupName=" + groupName)
    argv.append("releaseName=" + releaseName)
    argv.append("newReleaseName=" + newReleaseName)
    argv.append("isPatch=" + isPatch)
    argv.append("importApproval=" + importApproval)
    argv.append("project=" + project)
    argv.append("processingStep=" + process)
    #argv.append("output=xml")
    result = amiclient.execute(argv)
    print result.output()
    #print argv



except Exception, msg:
    print msg
