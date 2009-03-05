import sys
from pyAMI.pyAMI import *

class amiListProjects:
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
	        valid="AND projects.writeStatus='valid'"
	  if(len(argv)>0  and argv[0]=="-valid"):
	     valid="AND projects.writeStatus='valid'"   
	  if(len(argv)>0  and argv[0]=="-help"):
	     print " A command to list all ATLAS dataset project tags."   
             print " This command returns the project tag, the description, and a flag"
             print " to show if the project is a base project or not. "
             print " It also returns the project manager name, and the nomenclature used."
             print " The first argument can be a sub string to search on. "
             print " Use the option -valid to return only valid projects."
             print " Only those with writeStatus=valid can be used for new names."
	     return ["help"]
	  argument=[]
	  argument.append("SearchQuery")
	  argument.append("entity=projects")
	  argument.append("glite=SELECT projects.projectTag, projects.description, "+
                          "projects.isBaseType, projects.readStatus, "+
                          "projects.writeStatus, projects.projectManager, nomenclature.nomenclatureTemplate WHERE "+
                          "(projects.projectTag like '"+like+"') "+valid+" ORDER BY projectTag LIMIT 0,50")
	  argument.append("project=Atlas_Production")
	  argument.append("processingStep=*")
	  argument.append("mode=defaultField")
	  argument.extend(argv[i:])
	  return argument




def main(argv):
	
	
		try:
		      
			
			amiclient=AMI()
			result= amiclient.execute(amiListProjects().command(argv))		
			print result.output()
		
		except Exception, msg:	 
			print msg
 
		
if __name__=='__main__':
   main(sys.argv[1:])		
		
		
		
		
		
		
