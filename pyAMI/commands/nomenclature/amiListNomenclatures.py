import sys
from pyAMI.pyAMI import *

class amiListNomenclatures:
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
	        valid="AND nomenclature.writeStatus='valid'"
	  if(len(argv)>0  and argv[0]=="-valid"):
	     valid="AND nomenclature.writeStatus='valid'"   
	  if(len(argv)>0  and argv[0]=="-help"):
	     print " A command to list all ATLAS dataset nomenclature."   
             print " This command returns the nomenclature name, the template, and a tag. "
             print " The tag is used to associate nomenclature to projects."
             print " The first argument can be a sub string to search on. "
             print " Use the option -valid to return only valid nomenclature."
             print " Only those with writeStatus=valid can be used for new names."
	     return ["help"]
	  argument=[]
	  argument.append("SearchQuery")
	  argument.append("entity=nomenclature")
	  argument.append("glite=SELECT nomenclature.nomenclatureName, nomenclature.nomenclatureTemplate, nomenclature.nomenclatureTag WHERE (nomenclature.nomenclatureName like '"
                          +like+"') "+valid+" ORDER BY nomenclatureName LIMIT 0,50")
	  argument.append("project=Atlas_Production")
	  argument.append("processingStep=*")
	  argument.append("mode=defaultField")
	  argument.extend(argv[i:])
	  return argument




def main(argv):
	
	
		try:
		      
			
			amiclient=AMI()
			result= amiclient.execute(amiListNomenclatures().command(argv))		
			print result.output()
		
		except Exception, msg:	 
			print msg
 
		
if __name__=='__main__':
   main(sys.argv[1:])		
		
		
		
		
		
		
