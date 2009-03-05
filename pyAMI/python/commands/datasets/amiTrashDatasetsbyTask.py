import sys
from pyAMI.pyAMI import *

class amiTrashDatasetsbyTask:
	def __init__( self ):
		return 
	def command(self ,  argv):
		if len(argv)==0:
			raise AMI_Error( "You must provide a dataset name parameter. Use the \"-help\" option for more help" )
		limit="0,10"
		if(len(argv)>0  and argv[0]=="-help"):
			print " A command to trash datasets. \n Example \n"
			print " AMI TrashDatasetsbyTasks taskNum AMIUser=albrand AMIPass=notthisone trashAnnotation=something confirm=no"
			print " \nThe first argument must be a either \"-help\" or a task number"
			print " "
			print " The command first queries AMI to get a list of datasets matching the taskNumber"
			print " Then it asks for confirmation if the parameter confirm=no was not given."
			print " The user can optionally enter an annotation message." 
			print " "

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

	import getpass
	try:
                AMIUser=''
                AMIPass=''
                annotation=''
                thingsToRemove=[]
                confirm=True
                for thing in argv:
                   print thing 
	           if thing.startswith('AMIUser'):
		    AMIUser=thing[thing.find('=')+1:len(thing)]
		    thingsToRemove.append(thing)
		   if thing.startswith('AMIPass'):
		    AMIPass=thing[thing.find('=')+1:len(thing)]
		    thingsToRemove.append(thing)
		   if thing.startswith('trashAnnotation'):
		    annotation=thing[thing.find('=')+1:len(thing)]
		    print annotation
		    thingsToRemove.append(thing)
		   if thing.startswith('confirm=no'):
		    confirm=False
		    print confirm
		    thingsToRemove.append(thing)

		for thing in thingsToRemove:
                    argv.remove(thing)
                    
		amiclient=AMI()

		result= amiclient.execute(amiTrashDatasetsbyTask().command(argv))
		# find the datasets from the DOM object

		dom=result.getAMIdom()
		rowsets = dom.getElementsByTagName('rowset')
		infos = dom.getElementsByTagName('info')	
		for info in infos:
			# the first child gives the total number found
			print info.firstChild.nodeValue
		numFound = 0
		datasetsToTrash=[]
		for rowset in rowsets:
			rows = rowset.getElementsByTagName('row') 
			for row in rows:			   
				fields = row.getElementsByTagName('field') 
				for field in fields:
					fieldname=field.attributes['name'].value
					if (fieldname.lower()=='logicaldatasetname'):
						value=field.firstChild.nodeValue
						datasetsToTrash.append(value)
						numFound=numFound+1
						print value
                        if (confirm):
			   userInput=raw_input( "Do you want to trash these "+str(numFound)+" datasets? (Y/N)")
			else:
                           userInput='y'
			haveError=False
			if (userInput.lower()=="y"):
				#get back what we stored, to recheck permissions
                                if len(AMIUser)==0:                         
				   AMIUser=amiclient._client.pyAMICfg.get('AMI','AMIUser')
				if len(AMIPass)==0:   
				   AMIPass=amiclient._client.pyAMICfg.get('AMI','AMIPass')
				if(len(AMIUser)==0):
					AMIUser=raw_input('Please enter your AMIUser name : ')
				        AMIPass=getpass.getpass('Please enter your password : ')
				if(len(annotation)==0):        
				   annotation=raw_input( "Please enter a trashAnnotation comment : ")
				if(len(annotation)==0):
					annotation="trashed by "+AMIUser
				allargs=[] #common args for all the Trash commands
				
				allargs.append('ForceTrashDataset')
		
				allargs.append('-AMIUser='+AMIUser)
				allargs.append('-AMIPass='+AMIPass)
				allargs.append('-trashAnnotation='+annotation)
				# we use the default trashTrigger = 'By Administrator'
				# to stop resurrection
				allargs.append('-output=xml') #trick to treat errors correctly
				
				
				for dataset in datasetsToTrash:
					argument=[]
					argument.extend(allargs)
					argument.append('-logicalDatasetName='+dataset)
					try:
						
						result= amiclient.execute(argument )
						dom=result.getAMIdom()
						rstatus = dom.getElementsByTagName('commandStatus')
						for status in rstatus:
							print dataset+' trash was '+status.firstChild.nodeValue

					except Exception, msg:
						
						
							
						errormsg=str(msg)
						print errormsg[errormsg.find('<error>'):8+errormsg.find('</error>')]
						haveError=True
						break

			if(not haveError):
				print('All trashed')


	except Exception, msg:	 
		print msg


if __name__=='__main__':
	main(sys.argv[1:])		

