import sys
from pyAMI.pyAMI import *

class amiAddProductionStep:
   def __init__( self ):
      return 
   def command(self ,  argv):
	  argument=[]
	  argument.append("AddProductionStep")
	  argument.extend(argv)
	  return argument


def main(argv):
	
	
		try:
		      
			
			amiclient=AMI()
			result= amiclient.execute(amiAddProductionStep().command(argv))		
			print result.output()
		
		except Exception, msg:	 
			print msg
 
		
if __name__=='__main__':
   main(sys.argv[1:])		
		
		
		
		
		
		