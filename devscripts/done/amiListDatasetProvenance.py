import sys
from pyAMI import *

class amiListDatasetProvenance:
    """ A command to list dataset provenance.
      The first argument must be a either \"-help\" or a dataset name

      This second argument is a data type.
      If no data type is provided all data types are returned.
      The command returns also the generation number; +ve for a descendant, and
      -ve for an ancestor.
    """

    def __init__(self):
        return
    def command(self , argv):
        if len(argv) == 0:
            raise AMI_Error("You must provide a dataset name parameter")

        limit = "0,10"

        argument = []
        argument.append("ListDatasetProvenance")
        argument.append("logicalDatasetName=" + argv[0])
        argument.append('-output=xml')
        return argument



def main(argv):


    try:
        if((len(argv) > 0) and ((argv[0] == "-help")or (argv[0] == "help"))):
            print amiListDatasetProvenance.__doc__
            return None


        dataType = ""
        if(len(argv) > 1):
            dataType = argv[1]
        pyAMI_setEndPointType(argv)
        amiclient = AMI(False)
        result = amiclient.execute(amiListDatasetProvenance().command(argv))
        dom = result.getAMIdom()
        graph = dom.getElementsByTagName('graph')
        nFound = 0
        dictOfLists = {}
        for line in graph:
            nodes = line.getElementsByTagName('node')

            for node in nodes:
                level = int(node.attributes['level'].value)
                dataset = node.attributes['name'].value

                if (len(dataType) > 0)and(dataset.find(dataType) >= 0):
                    # print only selected dataType
                    levelList = dictOfLists.get(level, [])
                    levelList.append(dataset)
                    dictOfLists[level] = levelList
                    #print "generation =",level," ",dataset
                    nFound = nFound + 1
                elif (len(dataType) == 0):
                    #print everything
                    levelList = dictOfLists.get(level, [])
                    levelList.append(dataset)
                    dictOfLists[level] = levelList
                    #print level,dictOfLists[level]
                    nFound = nFound + 1

        if(nFound == 0)and (len(dataType) > 0):
            print "No datasets found of type", dataType
        else:
            keys = dictOfLists.keys()

            keys.sort()

        for key in keys:
            datasetList = dictOfLists.get(key)
            datasetList.sort()
            print "generation =", key
            for dataset in datasetList:
                print " ", dataset

    except Exception, msg:
        errormsg = str(msg)
        print errormsg



if __name__ == '__main__':
    main(sys.argv[1:])
