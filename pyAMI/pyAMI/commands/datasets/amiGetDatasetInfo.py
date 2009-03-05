import sys
from pyAMI.pyAMI import *
from pyAMI.commands.datasets.amiListDatasets import *
from string import rjust

class amiGetDatasetInfo:
   """
   This class is a wrapper to two AMI commands.
   It takes as its first argument a dataset name.
   If the dataset name is found in AMI a second command to the server
   produces all that is known about the dataset in AMI. ("expands" the child tables)
   By default the output is a list of parameter names and values.
   Parameter names with null values are omitted.
   Example:
   amiGetDatasetInfo misal1_mc12.006187.AlpgenJimmybbSlice1000Np3.simul.HITS.v12000605 
   If some other format is desired use the following syntax (here for xml output)
   amiGetDatasetInfo.py misal1_mc12.006187.AlpgenJimmybbSlice1000Np3.simul.HITS.v12000605 expand=off -output=xml

 """    
   def __init__( self ):
      return
   
       
   def command(self ,  argv):
	  if len(argv)<1:
		    raise AMI_Error( "You must provide a dataset name" )
	  
	  	 
	  amiclient=AMI()
	  
			
	  result= amiclient.execute(amiListDatasets().command(argv))		

	  #print result.output()
	  

	  dom=result.getAMIdom();
	  
	  argument=[]
	  argument.append("GetElementInfo")
	  argument.append("entityName=dataset")
	  
	  #Tell AMI which child tables must be expanded
	  # Here dataset_extra and event_range. "xsepx" is a Fulachierian Trick.
	  # Note that this is one of the few things in the AMI client which
	  # is schema dependent. If the schema has no table called "event_range"
	  # an exception is raised.
	 
	  rows = dom.getElementsByTagName('row')
	  
	  id=""
	  project=""
	  processingStep=""
	  
	  for row in rows:
	     fields = row.getElementsByTagName('field')  
	     for field in fields:
		#print field.attributes['name'].value
		if field.attributes['name'].value=="AMIELEMENTID":
	           id=field.firstChild.nodeValue
		   #print id
	        if field.attributes['name'].value=="PROJECT":
		   project=field.firstChild.nodeValue
		   #print project
                if field.attributes['name'].value=="PROCESS":
		   processingStep=field.firstChild.nodeValue
		   #print processingStep
	  argument.append("elementID="+id)
	  argument.append("project="+project)
	  argument.append("processingStep="+processingStep)
	  argument.extend(argv[1:])
	  return argument



def main(argv):
	
	
		try:
		        expand=True
		        
			if len(argv)<1:                     
                            raise AMI_Error( "You must provide a dataset name" )
		        if(argv[0]=="-help"):
                            print amiGetDatasetInfo.__doc__
                            return
		        if len(argv)>1:
                            if((argv[1]=="expand=OFF")|(argv[1]=="-expand=OFF")|(argv[1]=="expand=off")):
                                expand=False
                            #any other arguments ignored    
                            del argv[1]
			amiclient=AMI()
			if( expand):
                            argv.append("0,1")
                            argv.append("expandedChildren=dataset_extraxsepxevent_range" )
			result= amiclient.execute(amiGetDatasetInfo().command(argv))		
			if(not expand):
                            print result.output()
                        else:    
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
                                print "Parameters of dataset"
                                print "====================="
                                # looking at dataset table. Lots of fields in one row
                                for row in rows:
                                    fields = row.getElementsByTagName("field")
                                    for field in fields:
                                        value=""
                                        if field.firstChild:
						value=field.firstChild.nodeValue
						name = field.attributes['name'].value
                                                spaces=rjust(" ",30-len(name))
                                                print name+spaces+value
                                    
                            elif (rowsetLabel=="Element_Child"):
                                print ""
                                # what's the child name?
                            elif (rowsetLabel=="event_range") :
                                print "\nParameters of related task(s)"
                                print "==========================="
                                #  Lots of fields in each row
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
		
		
		
		
		
		
		
