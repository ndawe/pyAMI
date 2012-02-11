import sys
from pyAMI import *

class amiListProjects:
    """
        A command to list all ATLAS dataset project tags.
        This command returns the project tag, the description, and a flag
        to show if the project is a base project or not.
        It also returns the project manager name, and the nomenclature used.
        The first argument can be a sub string to search on.
        Use the option -valid to return only valid projects.
        Only those with writeStatus=valid can be used for new names.

    """
    def __init__(self):
        return
    def command(self , argv):

        i = 0
        like = "%"
        valid = ""
        if len(argv) > 0 and argv[0][0] != '-':
            like = "%" + argv[0] + "%"
            i = 1
        if(len(argv) > 1  and argv[1] == "-valid"):
            valid = "AND projects.writeStatus='valid'"
        if(len(argv) > 0  and argv[0] == "-valid"):
            valid = "AND projects.writeStatus='valid'"

        argument = []
        argument.append("SearchQuery")
        argument.append("entity=projects")
        argument.append("glite=SELECT projects.projectTag, projects.description, " +
                         "projects.isBaseType, projects.readStatus, " +
                         "projects.writeStatus, projects.projectManager, nomenclature.nomenclatureTemplate WHERE " +
                         "(projects.projectTag like '" + like + "') " + valid + " ORDER BY projectTag LIMIT 0,50")
        argument.append("project=Atlas_Production")
        argument.append("processingStep=*")
        argument.append("mode=defaultField")
        argument.extend(argv[i:])
        return argument




def main(argv):


    try:
        if(len(argv) > 0  and ((argv[0] == "-help")or (argv[0] == "help"))):
            print amiListProjects.__doc__
            return None

        pyAMI_setEndPointType(argv)
        amiclient = AMI()
        argv=amiclient.setUserCredentials(argv)
        result = amiclient.execute(amiListProjects().command(argv))
        print result.output()

    except Exception, msg:
        print msg


if __name__ == '__main__':
    main(sys.argv[1:])
