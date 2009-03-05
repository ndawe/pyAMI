import sys
from pyAMI.pyAMI import *

class amiListSubDataTypes:
   def __init__( self ):
      return 
   def command(self ,  argv):
	 	
	  i=0
	  like="%"
	  valid=""
	  if len(argv)>0 and argv[0][0]!='-':
	     like="%"+argv[0]+"%"
	     i=1
	     if(len(argv)>1  and argv[1]=="-valid"):
	        valid="AND subData_type.writeStatus='valid'"
	  if(len(argv)>0  and argv[0]=="-valid"):
	     valid="AND subData_type.writeStatus='valid'"   
	  if(len(argv)>0  and argv[0]=="-help"):
	     print " A command to list all ATLAS subDataTypes."
	     print " Only those with writeStatus=valid can be used for new compound dataTypes."
             print " The first argument can be a sub string to search on. "
             print " Use the option -valid to return only valid subDataTypes."
	     return ["help"]
	  argument=[]
	  argument.append("SearchQuery")
	  argument.append("entity=subData_type")
	  argument.append("glite=SELECT subData_type.subDataType, subData_type.description, subData_type.readStatus, subData_type.writeStatus WHERE (subData_type.subDataType like '"
                          +like+"') "+valid+" ORDER BY subDataType LIMIT 0,50")
	  argument.append("project=Atlas_Production")
	  argument.append("processingStep=*")
	  argument.append("mode=defaultField")
	  argument.extend(argv[i:])
	  return argument




def main(argv):
	
	
		try:
		      
			
			amiclient=AMI()
			result= amiclient.execute(amiListSubDataTypes().command(argv))		
			print result.output()
		
		except Exception, msg:	 
			print msg
 
		
if __name__=='__main__':
   main(sys.argv[1:])		
		
		
		
		
		
		
