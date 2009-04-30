import sys
import datetime
# The following is a mic mac until I change the package 
# structure in my public area to make it compatible with CMT
try :
  from pyAMI.pyAMI import *
except: 
  from pyAMI import *  

class amiQueryDatasets:
    """
     This class is a wrapper to an AMI Search.
     It will list datasets which match the criteria given.
     All criteria will be used in partial string searches.
     example
      amiQueryDatasets AtlasRelease=15 dataType=AOD version=%r651
      amiQueryDatasets dataType=AOD projectName=data08_cosmag runNumber=90345
      
      will map to the SQL predicates
      
      AtlasRelease like '15' AND dataType like 'AOD' AND version like '%r651'
      and
      dataType like 'AOD' AND projectName like 'data08_cosmag' AND runNumber like '90345'
      
      respectively.
      
      Use the "%" character to search for substrings
      amiQueryDatasets version=%r76%
      maps to 
      version like '%r76%'
      
      Only datasets which are VALID in AMI will be returned.
      It should be obvious how to change the script to change this behaviour!
      
      If more than 5000 results are obtained the query will loop getting 1000 max at a time, until all are retreived.
      

    """ 
    _predicate = ""  
    #lastModified > to_date('2009-01-01 00:00:00','yyyy-mm-dd hh24:mi:ss')
    
    def __init__(self):
        self._predicate = ""
        #self._isoDateFormat="yyyy-mm-dd hh24:mi:ss"
        return
    def getPredicate( self):
        return self._predicate[self._predicate.find("(1=1)")+9:]
        
    def command(self , argv, limit="0,10"):
        if len(argv) == 0:
            raise AMI_Error("You must provide some search parameters")
        
        if(len(argv) > 0  and argv[0] == "-help"):
            print amiQueryDatasets.__doc__
            return 
        
        argument = []
        argument.append("SearchQuery")
        argument.append("entity=dataset")
        self._predicate = "(1=1)"
        for arg in argv:
            egalindex = arg.find("=")
            paramName = arg[0:egalindex]
            paramValue = arg[egalindex + 1:]
            if(paramName=="lastModified"):
                #self._predicate = self._predicate + " AND "+"lastModified > to_date('2009-03-01 00:00:00','yyyy-mm-dd hh24:mi:ss')"
                self._predicate = self._predicate + " AND  lastModified >'"+paramValue+"'"
            else:
                #paramValue = paramValue + "%"
                self._predicate = self._predicate + " AND " + paramName + " like '" + paramValue + "'"
            
        argument.append("glite=SELECT logicalDatasetName WHERE amiStatus='VALID' AND " + self._predicate + " LIMIT " + limit)

        argument.append("project=Atlas_Production")
        argument.append("processingStep=Atlas_Production")
        argument.append("mode=defaultField")
        
        return argument




def main(argv):
   startLimit = 0
  # This number is the max to be returned by one request.
  # to avoid SOAP explosion
  # If there are more then we must resend the request.
   amountToDo = 5000
   datasetsToList = []
   try:
    amiclient = AMI()
    query = amiQueryDatasets()
    finished = False
    numDone = 0
    numToDo = 0
    
    while (not finished):
        result = amiclient.execute(query.command(argv, str(startLimit) + "," + str(amountToDo)))
        
        dom = result.getAMIdom()        
        rowsets = dom.getElementsByTagName('rowset')
        infos = dom.getElementsByTagName('info')   
        for info in infos:
         # the first child gives the total number found: example
         #"View 100 records, starting from row 1 of 2653 records "
         #print info.firstChild.nodeValue
         
            # take a look at the results each time - as the number may have changed between two queries
         ofIndex = info.firstChild.nodeValue.find("of")
         if(ofIndex <0 ):
             numToDo=0
         else :
             numDone = amountToDo + numDone   
             recordsIndex = info.firstChild.nodeValue.find("records", ofIndex)
             numToDo = info.firstChild.nodeValue[ofIndex + 2:recordsIndex - 1]
        
                
        finished = (int(numDone) >= int(numToDo))
     
        if(not finished):
                startLimit = startLimit + amountToDo
                
        if (numDone >0):
            numFound = 0
            for rowset in rowsets:
                rows = rowset.getElementsByTagName('row') 
                for row in rows:               
                    fields = row.getElementsByTagName('field') 
                    for field in fields:
                        fieldname = field.attributes['name'].value
                        if (fieldname.lower() == 'logicaldatasetname'):
                            value = field.firstChild.nodeValue
                            datasetsToList.append(value)
                            numFound = numFound + 1
    

    now = datetime.datetime.now()
    print "Request Time : " + now.strftime("%Y-%m-%d %H:%M")+ "\nRequest : "+ query.getPredicate()
            
    print str(numToDo) + " datasets found for this query"
    if (numDone >0):
        datasetsToList.sort()
        for dsn in datasetsToList:
            print dsn
   except Exception, msg:
         
        print msg


if __name__ == '__main__':
    main(sys.argv[1:])        





