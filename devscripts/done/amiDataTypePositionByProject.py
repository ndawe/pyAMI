import sys
from pyAMI import *
from string import split

class amiListDataTypePositionByProject:
    """
      Usage:
      amiListDataTypePositionByProject projectTag
      returns an integer which is the index of the dataType field in the nomenclature template
      for this project tag.      ( 1 = the first field)
      returns 0 if dataType is not used in the nomenclature for this project
      returns -1 if the project is known in AMI

    """
    def __init__(self):
        return
    def command(self , argv):

        if len(argv) > 0 and argv[0][0] != '-':
            projectTag = argv[0]


        argument = []
        argument.append("SearchQuery")
        argument.append("entity=nomenclature")
        argument.append("glite=SELECT nomenclature.nomenclatureTemplate WHERE projects.projectTag ='" +
                        projectTag + "'"
                           )
        argument.append("project=Atlas_Production")
        argument.append("processingStep=Atlas_Production")
        argument.append("mode=defaultField")

        return argument




def main(argv):


    try:
        if(len(argv) == 0):
            print amiListDataTypePositionByProject.__doc__
            return None
        if((len(argv) > 0) and ((argv[0] == "-help")or(argv[0] == "help"))):
            print amiListDataTypePositionByProject.__doc__
            return None

        pyAMI_setEndPointType(argv)
        amiclient = AMI()
        argv= amiclient.setUserCredentials(argv)
        result = amiclient.execute(amiListDataTypePositionByProject().command(argv))
        dom = result.getAMIdom()

        rowsets = dom.getElementsByTagName('rowset')
        if(len(rowsets) == 0) :
            print - 1
        for rowset in rowsets:
            rows = rowset.getElementsByTagName('row')
            for row in rows:
                fields = row.getElementsByTagName('field')
                for field in fields:
                    fieldname = field.attributes['name'].value
                    #print fieldname
                    if fieldname.lower() == 'nomenclaturetemplate':
                        nomenclaturetemplate = field.firstChild.nodeValue
                        nomenclatureFields = nomenclaturetemplate.split(".")
                        if "dataType" in nomenclatureFields:
                            print  nomenclatureFields.index("dataType") + 1
                        else:
                            print 0


    except Exception, msg:
        errormsg = str(msg)
        print errormsg

if __name__ == '__main__':
    main(sys.argv[1:])
