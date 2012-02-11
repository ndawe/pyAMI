import sys
from pyAMI import *

class amiListSubProjects:
    """
        This command lists all the sub projects. These are the second part of the project tags
        of the dataset names.
        The  first argument can be a part of name, so the search can be restricted.
        Example:
           amiListSubProjects GeV

    """
    def __init__(self):
        return
    def command(self , argv):

        i = 0
        like = "%"
        if len(argv) > 0 and argv[0][0] != '-':
            like = argv[0]
            i = 1

        argument = []
        argument.append("SearchQuery")
        argument.append("entity=subProjects")
        argument.append("glite=SELECT subProjects.subProjectTag, subProjects.description, subProjects.writeStatus, subProjects.readStatus, subProjects.createdBy  WHERE (subProjects.subProjectTag like '%" + like + "%') AND subProjects.writeStatus='valid' ORDER BY subProjectTag LIMIT 0,50")
        argument.append("project=Atlas_Production")
        argument.append("processingStep=*")
        argument.append("mode=defaultField")
        argument.extend(argv[i:])
        return argument




def main(argv):

    try:
        if(len(argv) > 0  and ((argv[0] == "-help")or (argv[0] == "help"))):
            print amiListSubProjects.__doc__
            return None

        pyAMI_setEndPointType(argv)
        amiclient = AMI()
        argv=amiclient.setUserCredentials(argv)
        result = amiclient.execute(amiListSubProjects().command(argv))
        print result.output()

    except Exception, msg:
        print msg

if __name__ == '__main__':
    main(sys.argv[1:])
