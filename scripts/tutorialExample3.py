import sys
import setup_pyAMI
 # the above line needed to ensure correct python environment since pyAMI 4.0.3
from pyAMI.client import AMIClient
class test3:
    def main(argv):
        
        arguments = []
        arguments.append("SearchQuery")
        arguments.append("glite=select logicalDatasetName, totalEvents where (amiStatus='VALID' AND dataset.prodsysStatus='ALL EVENTS AVAILABLE' AND dataset.dataType='AOD' AND dataset.logicalDatasetName LIKE 'data12%merge%' and totalEvents > 6000000)"  )
        arguments.append("project=Atlas_Production")
        arguments.append("processingStep=Atlas_Production")
        arguments.append("entity=dataset")
        amiClient = AMIClient()
        
        try:
            result=amiClient.execute(arguments)
            # in csv just for fun
            print result.output('csv')
        except Exception, msg:
            error = str(msg)
            print error
   
    if __name__ == '__main__':
        main(sys.argv[1:])  
 
