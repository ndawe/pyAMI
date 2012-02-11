import sys
from pyAMI import *

class amiListDatasetsbyFile:
    """
       A command to list the dataset which contains the given file.
       The first argument must be a either \"-help\" or a file name.

       By default only valid datasets are returned. (It should be obvious how to modify the wrapper to change this behaviour)
       To search in archived catalogues as well use the option \"-showArchived=true\"
       This command is an example of wrapping a gLite query to AMI.
       The python wrapper can be taken as a model for all queries to AMI.

       See  amiListDatasets for another example.
    """
    def __init__(self):
        return
    def command(self , argv):
        if len(argv) == 0:
            raise AMI_Error("You must provide a filename (LFN)")

        argument = []
        argument.append("SearchQuery")
        argument.append("entity=dataset")

        argument.append("glite=SELECT logicalDatasetName,files.fileGUID WHERE amiStatus='VALID'  AND files.LFN = '" + argv[0] +"'")

        argument.append("project=Atlas_Production")
        argument.append("processingStep=Atlas_Production")

        argument.extend(argv[1:])
        return argument




def main(argv):


    try:
        if(len(argv) > 0  and ((argv[0] == "-help")or (argv[0] == "help"))):
            print amiListDatasetsbyFile.__doc__
            return None
        pyAMI_setEndPointType(argv)
        amiclient = AMI()
        result = amiclient.execute(amiListDatasetsbyFile().command(argv))
        print result.output()

    except Exception, msg:
        print msg


if __name__ == '__main__':
    main(sys.argv[1:])
