import sys
from pyAMI.pyAMI import *

class amiListDatasetsbyTask:
   def __init__( self ):
      return 
   def command(self ,  argv):
	  if len(argv)==0:
		    raise AMI_Error( "You must provide a task number" )
	  limit="0,10"
	  if(len(argv)>0  and argv[0]=="-help"):
	     print " A command to list datasets."
	     print " The first argument must be a either \"-help\" or prodSys task number. "
             print "  "
             print " By default only valid datasets are returned."
             print " No information is currently returned about the status of the task."
             print " This command is an example of wrapping a gLite query to AMI."
             print " The python wrapper can be taken as a model for all queries to AMI."
             print " See  amiListDatasets for another example."
	     return ["help"]
	  if len(argv)>1 and argv[1][0]!='-':
	  	    limit=argv[1]
	  argument=[]
	  argument.append("SearchQuery")
	  argument.append("entity=dataset")
	  
	  argument.append("glite=SELECT logicalDatasetName WHERE amiStatus='VALID'  AND event_range.prodsysIdentifier = '"+argv[0]+"' LIMIT "+limit)
	  
	  argument.append("project=Atlas_Production")
	  argument.append("processingStep=Atlas_Production")
	  argument.append("mode=defaultField")
	  argument.extend(argv[1:])
	  return argument




def main(argv):
	
	
		try:
		      
			
			amiclient=AMI()
			result= amiclient.execute(amiListDatasetsbyTask().command(argv))		
			print result.output()
		
		except Exception, msg:	 
			print msg
 
		
if __name__=='__main__':
   main(sys.argv[1:])		
		
		
		
		
		
		
