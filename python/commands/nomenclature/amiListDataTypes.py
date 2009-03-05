import sys
from pyAMI.pyAMI import *

class amiListDataTypes:
   def __init__( self ):
      return 
   def command(self ,  argv):
	# This is class shows how a glite query can be sent to AMI
	# The "entity" parameter is set to the type of the thing one
	# wants to search for.
	# The project and process can be set to * to search over all AMI catalogues
	# In this case we know we are searching for one of the global objects
	# - so we can give the project name explicitly.
	#################################
	  i=0
	  like="%"
	  valid=""
	  if len(argv)>0 and argv[0][0]!='-':
	     like="%"+argv[0]+"%"
	     i=1
	     if(len(argv)>1  and argv[1]=="-valid"):
	        valid="AND data_type.writeStatus='valid'"
	  if(len(argv)>0  and argv[0]=="-valid"):
	     valid="AND data_type.writeStatus='valid'"   
	  if(len(argv)>0  and argv[0]=="-help"):
	     print " A command to list all ATLAS dataTypes."
	     print " Only those with writeStatus=valid can be used for new names."
             print " The first argument can be a sub string to search on. "
             print " Use the option -valid to return only valid dataTypes."
	     return ["help"]
	  
	  argument=[]
	  argument.append("SearchQuery")
	  argument.append("entity=data_type")
	  argument.append("glite=SELECT data_type.dataType, data_type.description, data_type.writeStatus, data_type.readStatus WHERE (data_type.dataType like '"
                          +like+"') "+valid+" ORDER BY dataType LIMIT 0,50")
	  argument.append("project=Atlas_Production")
	  argument.append("processingStep=*")
	  argument.append("mode=defaultField")
	  argument.extend(argv[i:])
	  return argument




def main(argv):
	
	
		try:
		      
			
			amiclient=AMI()
			result= amiclient.execute(amiListDataTypes().command(argv))		
			print result.output()
		
		except Exception, msg:	 
			print msg
 
		
if __name__=='__main__':
   main(sys.argv[1:])		
		
		
		
		
		
		
