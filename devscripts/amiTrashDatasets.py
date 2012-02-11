import sys
from pyAMI import *

class amiTrashDatasets:
    def __init__(self):
        return 
    def command(self , argv):
        if len(argv) == 0:
            raise AMI_Error("You must provide a dataset name parameter. Use the \"-help\" option for more help")
        limit = "0,10"
        if(len(argv) > 0  and argv[0] == "-help"):
            print " A command to trash datasets. \n Example \n"
            print " AMI TrashDatasets calib1_mc12.00700%.singlepart_e_Et%.recon.%v12003104 AMIUser=albrand AMIPass=notthisone"
            print " \nThe first argument must be a either \"-help\" or a dataset name"
            print " or part of a dataset name. Use the % character for wild carding "
            print " The command first queries AMI to get a list of datasets matching the pattern"
            print " Then it asks for confirmation."
            print " The user can optionally enter an annotation message." 
            print " By default the annotation message will be the name of the user"
            print " As with all AMI commands, by default only 10 rows are treated at a time."
            print " To override this limit please use the parameter \"-limit.\""
            print " for example \"-limit=0,30\" will get 30 rows starting from row 0"

            return ["help"]
        if len(argv) > 1 and argv[1][0] != '-': 
            limit = argv[1]
        argument = []
        argument.append("SearchQuery")
        argument.append("entity=dataset")

        argument.append("glite=SELECT logicalDatasetName WHERE amiStatus='VALID' AND logicalDatasetName like '" + argv[0] + "' LIMIT " + limit)

        argument.append("project=Atlas_Production")
        argument.append("processingStep=Atlas_Production")
        argument.append("mode=defaultField")
        argument.extend(argv[1:])
        return argument




def main(argv):

    import getpass
    try:
        pyAMI_setEndPointType(argv)
        amiclient = AMI()

        result = amiclient.execute(amiTrashDatasets().command(argv))
        # find the datasets from the DOM object

        dom = result.getAMIdom()
        rowsets = dom.getElementsByTagName('rowset')
        infos = dom.getElementsByTagName('info')        
        for info in infos:
            # the first child gives the total number found
            print info.firstChild.nodeValue
        numFound = 0
        datasetsToTrash = []
        for rowset in rowsets:
            rows = rowset.getElementsByTagName('row') 
            for row in rows:                           
                fields = row.getElementsByTagName('field') 
                for field in fields:
                    fieldname = field.attributes['name'].value
                    if (fieldname.lower() == 'logicaldatasetname'):
                        value = field.firstChild.nodeValue
                        datasetsToTrash.append(value)
                        numFound = numFound + 1
                        print value

            userInput = raw_input("Do you want to trash these " + str(numFound) + " datasets? (Y/N)")
            haveError = False
            if (userInput.lower() == "y"):
                #get back what we stored, to recheck permissions
                AMIUser = amiclient._client.pyAMICfg.get('AMI', 'AMIUser')
                AMIPass = amiclient._client.pyAMICfg.get('AMI', 'AMIPass')
                if(len(AMIUser) == 0):
                    AMIUser = raw_input('Please enter your AMIUser name : ')
                    AMIPass = getpass.getpass('Please enter your password : ')
                annotation = raw_input("Please enter a trashAnnotation comment : ")
                if(len(annotation) == 0):
                    annotation = "trashed by " + AMIUser
                allargs = [] #common args for all the Trash commands
                
                allargs.append('ForceTrashDataset')

                allargs.append('-AMIUser=' + AMIUser)
                allargs.append('-AMIPass=' + AMIPass)
                allargs.append('-trashAnnotation=' + annotation)
                # we use the default trashTrigger = 'By Administrator'
                # to stop resurrection
                allargs.append('-output=xml') #trick to treat errors correctly
                
                
                for dataset in datasetsToTrash:
                    argument = []
                    argument.extend(allargs)
                    argument.append('-logicalDatasetName=' + dataset)
                    try:
                            
                        result = amiclient.execute(argument)
                        dom = result.getAMIdom()
                        rstatus = dom.getElementsByTagName('commandStatus')
                        for status in rstatus:
                            print dataset + ' trash was ' + status.firstChild.nodeValue

                    except Exception, msg:
                            
                            
                                    
                        errormsg = str(msg)
                        print errormsg[errormsg.find('<error>'):8 + errormsg.find('</error>')]
                        haveError = True
                        break

            if(not haveError):
                print('All trashed')


    except Exception, msg:   
        print msg


if __name__ == '__main__':
    main(sys.argv[1:])              

