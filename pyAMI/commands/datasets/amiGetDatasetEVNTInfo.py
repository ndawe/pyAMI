import sys
from pyAMI import *
from commands.datasets.amiGetDatasetInfo import *
from commands.datasets.amiListDatasetProvenance import *
from string import rjust

class amiGetDatasetEVNTInfo:
   """
   This class is a wrapper to three AMI WS commands in two other wrappers.
   It takes as its first argument a dataset name.
   The fist call  produces selected info about the EVNT dataset, 
   parent of the input parameter . Then we use this dataset name as input to
   another wrapper which "expands" the child tables.
   By default the output is a list of parameter names and values.
   Parameter names with null values are omitted.
   Example:

   amiGetDatasetEVNTInfo.py mc08.106031.McAtNloWminenu_1Lepton.simul.HITS.e384_s462 

 """    
def __init__( self ):
      return
   
       


def main(argv):

     
      if((len(argv)>0)and (argv[0]=="-help")):
	    print amiGetDatasetEVNTInfo.__doc__
	    return	
      
	 
	   
      try:
	 if len(argv)<1:
	    raise AMI_Error( "<error>You must provide a dataset name as the first parameter</error>" )
	    #argv.append('mc08.106031.McAtNloWminenu_1Lepton.simul.HITS.e384_s462')
	 dataType="EVNT"              
	 amiclient=AMI()
	 # This command returns the complete production tree
	 result= amiclient.execute(amiListDatasetProvenance().command(argv))
	 dom = result.getAMIdom()
	 graph = dom.getElementsByTagName('graph')
	 nFound = 0
	 dictOfLists={}
	 for line in graph:
	    nodes = line.getElementsByTagName('node')
		  
	    for node in nodes:
	       level=int(node.attributes['level'].value)
	       dataset = node.attributes['name'].value
		     
	       if (len(dataType)>0)and(dataset.find(dataType)>=0):
			# print only selected dataType
		  levelList=dictOfLists.get(level,[])
		  levelList.append(dataset)
		  dictOfLists[level] = levelList 
		  #print "generation =",level," ",dataset
		  nFound=nFound+1
		  
	    if(nFound==0):
		  print "No datasets found of type",dataType
	    else:
		  keys = dictOfLists.keys()
		   
		  keys.sort()
		   
		  for key in keys:
		     datasetList=dictOfLists.get(key)
		     # datasetList.sort()
		     # actually there's only one in the list
		     for dataset in datasetList:
			print "EVGEN dataset = ",dataset 
		     
	       
      except Exception, msg:   
	       errormsg=str(msg)
	       print errormsg[errormsg.find('<error>'):8+errormsg.find('</error>')]
	       return
						   
      try:
	 # when we get here "dataset" contains the name of the parent dataset
	 # find out some more about it using the GetDatasetInfo command
	    expand=True
	    argv=[]
	    argv.append(dataset)
   
	    argv.append("0,1")
	    argv.append("expandedChildren=dataset_extraxsepxdataset_comment" )
	    result= amiclient.execute(amiGetDatasetInfo().command(argv))		
      
	    dom=result.getAMIdom()
			     # get the rowsets
	    rowsets = dom.getElementsByTagName('rowset')
	    for rowset in rowsets:
	       rowsetLabel=""
	       if "type" in rowset.attributes.keys():
		  rowsetLabel=rowsetLabel+rowset.attributes['type'].value
		  # expecting either "Element_Info" or "Element_Child" or a child name
		  rows = rowset.getElementsByTagName('row')
		  if (rowsetLabel=="Element_Info"):
		     print ""
		     ## Don't bother to list all the dataset parameters
		     ## Uncomment the block if you want to.
		     #print "Parameters of dataset"
		     #print "====================="
		  ## looking at dataset table. Lots of fields in one row
		     #for row in rows:
			#fields = row.getElementsByTagName("field")
			#for field in fields:
			   #value=""
			   #if field.firstChild:
				    #value=field.firstChild.nodeValue
				    #name = field.attributes['name'].value
				    #spaces=rjust(" ",30-len(name))
				    #print name+spaces+value
				       
		  elif (rowsetLabel=="Element_Child"):
			      print ""
				    # what's the child name? we were not expecting it
		  elif (rowsetLabel=="dataset_comment") :
				 print "\nAdded Comments(s)"
				 print "==========================="
				   #  should be 3 fields in each row
				   # don't know how many rows - depends who put what!
				 for row in rows:
				       fields = row.getElementsByTagName("field")
				       for field in fields:
					  fieldName = field.attributes['name'].value
					  if((fieldName!="PROJECT")&(fieldName!="PROCESS")
					      &(fieldName!="AMIENTITYNAME")&(fieldName!="AMIELEMENTID")):
						value=""
						if field.firstChild:
						   value=field.firstChild.nodeValue
						   print fieldName+rjust(" ",30-len(fieldName))+value
				       print ""            
		  elif (rowsetLabel=="dataset_extra") :
				    print "\nExtra Parameters"
				    print "==========================="
				   #  Lots of rows one field in each
				    for row in rows:
				       fields = row.getElementsByTagName("field")
				       for field in fields:
					  fieldName = field.attributes['name'].value
					  if (fieldName=="field"):
					     fieldNameToPrint = field.firstChild.nodeValue
					  elif (fieldName=="value"):
					     valueToPrint = field.firstChild.nodeValue
				       print fieldNameToPrint+rjust(" ",30-len(fieldNameToPrint))+valueToPrint       
			       
		  elif (rowsetLabel=="Element_PhysicsProperties") :
				    print "\nOther Physics Properties"
				    print "==========================="
				    for row in rows:
				       fields = row.getElementsByTagName("field")
				       description=""
				       unit=""
				       minVal=""
				       maxVal=""
				       for field in fields:
					  fieldName=field.attributes['name'].value
					   #print fieldName
					  if(fieldName=="propertyName"):
						fieldNameToPrint = field.firstChild.nodeValue
					  elif(fieldName=="propertyDescription"):
						if field.firstChild:
						   description = field.firstChild.nodeValue
					  elif(fieldName=="propertyUnit"):
						if field.firstChild:
						   unit = "("+field.firstChild.nodeValue+")"
					  elif(fieldName=="propertyMinValue"):
						minVal = field.firstChild.nodeValue
						#print minVal
					  elif(fieldName=="propertyMaxValue"):
						maxVal = field.firstChild.nodeValue
						#print maxVal
				       #print minVal,maxVal,(minVal==maxVal) 
				       if (minVal==maxVal):
					  valueToPrint=minVal 
				       else:
					  valueToPrint=">= "+minVal+", <="+maxVal
   
				       print  fieldNameToPrint+rjust(" ",30-len(fieldNameToPrint))+valueToPrint + unit+" "+description       
		   
      except Exception, msg:	 
			   print msg
    
		   
if __name__=='__main__':
   main(sys.argv[1:])		
		
		
		
		
		
		
		
