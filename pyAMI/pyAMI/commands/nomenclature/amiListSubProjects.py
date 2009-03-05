import sys
from pyAMI.pyAMI import *

class amiListSubProjects:
   def __init__( self ):
      return 
   def command(self ,  argv):
	 	
	  i=0
	  like="%"   	  
	  if len(argv)>0 and argv[0][0]!='-':
	     like=argv[0]
	     i=1
	  if(len(argv)>0  and argv[0]=="-help"):
	     print " first argument can a part of name, you can use -limit=x,y"
	     return ["help"]
	  argument=[]
	  argument.append("SearchQuery")
	  argument.append("entity=subProjects")
	  argument.append("glite=SELECT subProjects.subProjectTag, subProjects.description, subProjects.writeStatus, subProjects.readStatus, subProjects.createdBy  WHERE (subProjects.subProjectTag like '"+like+"') AND subProjects.writeStatus='valid' ORDER BY subProjectTag LIMIT 0,50")
	  argument.append("project=Atlas_Production")
	  argument.append("processingStep=*")
	  argument.append("mode=defaultField")
	  argument.extend(argv[i:])
	  return argument




def main(argv):
	
	
		try:
		      
			
			amiclient=AMI()
			result= amiclient.execute(amiListSubProjects().command(argv))		
			print result.output()
		
		except Exception, msg:	 
			print msg
 
		
if __name__=='__main__':
   main(sys.argv[1:])		
		
		
		
		
		
		