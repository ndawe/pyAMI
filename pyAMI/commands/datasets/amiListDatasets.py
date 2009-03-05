import sys
from pyAMI.pyAMI import *

class amiListDatasets:
	def __init__( self ):
		return 
	def command(self ,  argv):
		if len(argv)==0:
			raise AMI_Error( "You must provide a dataset name parameter" )
		limit="0,10"
		if(len(argv)>0  and argv[0]=="-help"):
			print " A command to list datasets."
			print " The first argument must be a either \"-help\" or a dataset name"
			print " or part of a dataset name. Use the % character for wild carding "
			print " By default only valid datasets are returned."
			print " This command is an example of wrapping a gLite query to AMI."
			print " The python wrapper can be taken as a model for all queries to AMI."
			print " See  amiListDatasetsbyTask for another example."
			return ["help"]
		if len(argv)>1 and argv[1][0]!='-': 
			limit=argv[1]
		argument=[]
		argument.append("SearchQuery")
		argument.append("entity=dataset")

		argument.append("glite=SELECT logicalDatasetName WHERE amiStatus='VALID' AND logicalDatasetName like '%"+argv[0]+"%' LIMIT "+limit)

		argument.append("project=Atlas_Production")
		argument.append("processingStep=Atlas_Production")
		argument.append("mode=defaultField")
		argument.extend(argv[1:])
		return argument




def main(argv):


	try:


		amiclient=AMI()
		result= amiclient.execute(amiListDatasets().command(argv))		
		print result.output()

	except Exception, msg:	 
		print msg


if __name__=='__main__':
	main(sys.argv[1:])		






