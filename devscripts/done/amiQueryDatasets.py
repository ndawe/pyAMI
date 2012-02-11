import sys
import datetime
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

      AtlasRelease like '15%' AND dataType like 'AOD%' AND version like '%r651%'
      and
      dataType like 'ESD%' AND projectName like 'data08_cosmag%' AND runNumber like '90345%'

      respectively.

      Put a leading "%" character to search for substrings
      amiQueryDatasets version=%r76
      maps to
      version like '%r76%'

      Only datasets which are VALID in AMI will be returned.
      It should be obvious how to change the script to change this behaviour!

      Two additional arguments
      lastModifiedAfter and lastModifiedBefore
      permit the restriction of results by date
      Example
        lastModifiedBefore=\"2009-12-11 00:47:14\"
       Use exactly the above format for timestamps, and as there is a space in the value, enclose with \"\"
      If more than 5000 results are obtained the query will loop getting 1000 max at a time, until all are retreived.


    """

    _predicate = ""

    def __init__(self):
        self._predicate = ""
        return

    def getPredicate(self):
        return self._predicate[self._predicate.index("AND") + 4:]

    def command(self , argv, limit="0,10"):
        if not argv or len(argv) == 0:
            raise AMI_Error("You must provide some search parameters ")
        argument = []
        argument.append("SearchQuery")
        argument.append("entity=dataset")
        for arg in argv:
            egalindex = arg.find("=")
            paramName = arg[0:egalindex]
            if paramName == "lastModifiedAfter":
                paramValue = arg[egalindex + 1:]
                self._predicate = self._predicate + " AND lastModified>'" + paramValue + "'"
            elif paramName == "lastModifiedBefore":
                paramValue = arg[egalindex + 1:]
                self._predicate = self._predicate + " AND lastModified<'" + paramValue + "'"
            else:
                paramValue = arg[egalindex + 1:] + "%"
                self._predicate = self._predicate + " AND " + paramName + " like '" + paramValue + "'"
            # other parameters could be selected also, "SELECT logicalDatasetName,lastModified" for eaxample
            # and then change the result parsing to see them.
        argument.append("glite=SELECT logicalDatasetName WHERE amiStatus='VALID'" + self._predicate + " LIMIT " + limit)
        argument.append("project=Atlas_Production")
        argument.append("processingStep=Atlas_Production")

        return argument




def main(argv):


    if ((len(argv) > 0)  and ((argv[0] == "-help") or (argv[0] == "help"))):
        print amiQueryDatasets.__doc__
        return None
    startLimit = 0
    # This number is the max to be returned by one request.
    # to avoid SOAP explosion
    # If there are more then we must resend the request.
    amountToDo = 5000
    datasetsToList = []
    try:
        pyAMI_setEndPointType(argv)
        amiclient = AMI()
        argv=amiclient.setUserCredentials(argv)
        query = amiQueryDatasets()
        finished = False
        numDone = 0
        numToDo = 0

        while not finished:

            result = amiclient.execute(query.command(argv, str(startLimit) + "," + str(amountToDo)))

            dom = result.getAMIdom()

            rowsets = dom.getElementsByTagName('rowset')
            infos = dom.getElementsByTagName('info')
            for info in infos:
                # the first child gives the total number found: example
                #"View 100 records, starting from row 1 of 2653 records "

                # take a look at the results each time - as the number may have changed between two queries

                ofIndex = info.firstChild.nodeValue.find("of")

                if ofIndex < 0 :
                    numToDo = 0
                else :
                    numDone = amountToDo + numDone
                    recordsIndex = info.firstChild.nodeValue.find("records", ofIndex)
                    numToDo = info.firstChild.nodeValue[ofIndex + 2:recordsIndex - 1]



            finished = (int(numDone) >= int(numToDo))

            if not finished:
                startLimit = startLimit + amountToDo

            if numDone > 0:
                numFound = 0
                for rowset in rowsets:
                    rows = rowset.getElementsByTagName('row')
                    for row in rows:
                        fields = row.getElementsByTagName('field')
                        for field in fields:
                            fieldname = field.attributes['name'].value

                            if fieldname.lower() == 'logicaldatasetname':
                                value = field.firstChild.nodeValue
                                datasetsToList.append(value)
                                numFound = numFound + 1


        now = datetime.datetime.now()
        print "Request Time : " + now.strftime("%Y-%m-%d %H:%M") + "\nRequest : " + query.getPredicate()

        print str(numToDo) + " datasets found for this query"
        if numDone > 0:
            datasetsToList.sort()
            for dsn in datasetsToList:
                print dsn
    except Exception, msg:
        print msg


if __name__ == '__main__':
    main(sys.argv[1:])
