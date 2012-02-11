import sys
from pyAMI import *

class amiListDatasetsbyTask:
    """ A command to list datasets.
       The first argument must be a either \"-help\" or prodSys task number.
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
            raise AMI_Error("You must provide a task number")

        argument = []
        argument.append("SearchQuery")
        argument.append("entity=dataset")
        # Notice the strength of the Glite grammar!
        # Some AMI schema use "event_range" for the task table and some use "prodsys_task"
        # This works for both schema types.
        argument.append("glite=SELECT logicalDatasetName WHERE amiStatus='VALID'  AND (event_range.prodsysIdentifier = '" + argv[0] + "')or(prodsys_task.prodsysIdentifier = '" + argv[0] + "')" )

        argument.append("project=Atlas_Production")
        argument.append("processingStep=Atlas_Production")
        argument.append("mode=defaultField")
        argument.extend(argv[1:])
        return argument




def main(argv):


    try:
        if(len(argv) > 0  and ((argv[0] == "-help")or (argv[0] == "help"))):
            print amiListDatasetsbyTask.__doc__
            return None
        pyAMI_setEndPointType(argv)
        amiclient = AMI()
        result = amiclient.execute(amiListDatasetsbyTask().command(argv))
        print result.output()

    except Exception, msg:
        print msg


if __name__ == '__main__':
    main(sys.argv[1:])
