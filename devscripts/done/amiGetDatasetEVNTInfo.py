import sys
from pyAMI import *
from amiListDatasetProvenance import *
from string import rjust


class amiGetDatasetEVNTInfo:
    """
    This class is a wrapper to three AMI WS commands in two other wrappers.
    It takes as its first argument a Monte Carlo dataset name.
    The fist call  produces selected info about the EVNT dataset,
    parent of the input parameter . Then we use this dataset name as input to
    another wrapper which "expands" the child tables.
    By default the output is a list of parameter names and values.
    Parameter names with null values are omitted.
    Example:

    amiGetDatasetEVNTInfo mc08.106031.McAtNloWminenu_1Lepton.simul.HITS.e384_s462

    """
    def __init__(self):
        return


def main(argv):

    try:
        if len(argv) < 1:
            raise AMI_Error("You must provide a Monte Carlo dataset name as the first parameter")
        if((len(argv) > 0)and ((argv[0] == "-help")or (argv[0] == "help"))):
            print amiGetDatasetEVNTInfo.__doc__
            return None

        inputDataset = argv[0]

        dataType = "EVNT"
        pyAMI_setEndPointType(argv)

        amiclient = AMI()
        argv=amiclient.setUserCredentials(argv)


        # This command returns the complete production tree
        result = amiclient.execute(amiListDatasetProvenance().command(argv))

        dom = result.getAMIdom()

        graph = dom.getElementsByTagName('graph')
        nFound = 0
        evgenDatasets = []
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
                    #print "generation =", level, " ", dataset

                    keys = dictOfLists.keys()

                    keys.sort()

                    for key in keys:
                        datasetList = dictOfLists.get(key)
                        # datasetList.sort()
                        # actually there's only one in the list
                        for dataset in datasetList:
                            evgenDatasets.append(dataset)
                            # print "EVGEN dataset = ", evgenDatasets

    except Exception, msg:
        errormsg = str(msg)
        print errormsg
        return

    if(len(evgenDatasets) == 0):
        print("No EVNT parent could be found for dataset " + inputDataset)
        return None
    for evgenDataset in set(evgenDatasets) :
        try:
            # when we get here "dataset" contains the name of the parent dataset
            # find out some more about it using the GetDatasetInfo command
            expand = True
            argv = []
            argv.append("GetDatasetInfo")
            #print dataset
            argv.append("logicalDatasetName=" + evgenDataset)


            result = amiclient.execute(argv)

            dom = result.getAMIdom()
            # get the rowsets
            rowsets = dom.getElementsByTagName('rowset')

            for rowset in rowsets:
                rowsetLabel = ""
                if "type" in rowset.attributes.keys():
                    rowsetLabel = rowsetLabel + rowset.attributes['type'].value
                    rows = rowset.getElementsByTagName('row')
                    if (rowsetLabel == "Element_Info"):
                        sDatasetInfo = ""
                        sDatasetAddedComment = ""
                        sDatasetExtra = ""
                        datasetPhysProp = {}

                        for row in rows:
                            fields = row.getElementsByTagName("field")
                            for field in fields:
                                if field.firstChild:
                                    tableName = field.attributes['table'].value
                                    # print tableName+"  "+evgenDataset
                                    if tableName == "dataset":
                                        value = field.firstChild.nodeValue
                                        name = field.attributes['name'].value
                                        spaces = rjust(" ", 30 - len(name))
                                        sDatasetInfo += name + spaces + value + "\n"
                                    elif tableName == "dataset_extra":
                                        value = field.firstChild.nodeValue
                                        name = field.attributes['name'].value
                                        spaces = rjust(" ", 30 - len(name))
                                        sDatasetExtra += name + spaces + value + "\n"
                                    elif (tableName == "dataset_added_comment")or(tableName == "dataset_comment"):
                                        value = field.firstChild.nodeValue
                                        name = field.attributes['name'].value
                                        spaces = rjust(" ", 30 - len(name))
                                        sDatasetAddedComment += name + spaces + value + "\n"
                                    elif  (tableName == "dataset_property"):

                                        propertyName = field.attributes['name'].value.split('_')[0]
                                        if datasetPhysProp.has_key(propertyName):
                                            tmpDict = datasetPhysProp.get(propertyName)
                                        else:
                                            tmpDict = {"type":"" , "min":"", "max":"", "unit":"", "description":""}
                                        propertyNameSubField = field.attributes['name'].value
                                        try :
                                            propertyNameSubValue = field.firstChild.nodeValue
                                        except Exception :
                                            propertyNameSubValue = ""
                                        if propertyNameSubField == propertyName + "_type":
                                            tmpDict["type"] = propertyNameSubValue
                                        if propertyNameSubField == propertyName + "_min":
                                            tmpDict["min"] = propertyNameSubValue
                                        if propertyNameSubField == propertyName + "_max":
                                            tmpDict["max"] = propertyNameSubValue
                                        if propertyNameSubField == propertyName + "_unit":
                                            tmpDict["unit"] = propertyNameSubValue
                                        if propertyNameSubField == propertyName + "_desc":
                                            tmpDict["description"] = propertyNameSubValue
                                        datasetPhysProp[propertyName] = tmpDict
                                        #print propertyName
                                        #if field.attributes['name'].value.contains("_type"):
                                        #   value=field.firstChild.nodeValue

                if sDatasetInfo != "":
                    print ""
                    print "Parameters of dataset"
                    print "====================="
                    print sDatasetInfo
                if sDatasetAddedComment != "":
                    print "Added Comments(s)"
                    print "====================="
                    print sDatasetAddedComment
                if sDatasetExtra != "":
                    print "Extra Parameters"
                    print "====================="
                    print sDatasetExtra
                if datasetPhysProp:
                    print "Other Physics Properties"
                    print "====================="
                    for physProp in datasetPhysProp.keys():
                        tmpDict = datasetPhysProp.get(physProp)
                        valueToPrint = ""
                        if tmpDict.get("min") == tmpDict.get("max"):
                            valueToPrint = tmpDict.get("min")
                        else:
                            valueToPrint = ">= " + tmpDict.get("min") + ", <=" + tmpDict.get("max")
                        print physProp + rjust(" ", 30 - len(physProp)) + " " + valueToPrint + " " + tmpDict.get("unit") + "   \"" + tmpDict.get("description") + "\""

        except Exception, msg:
            print msg


if __name__ == '__main__':
    main(sys.argv[1:])
