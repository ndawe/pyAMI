#!/usr/bin/python

from dq2.clientapi.DQ2 import DQ2
import sys, commands
from pyAMI.pyAMI import *

if __name__ == '__main__':

    if len(sys.argv)>1:
        containername = sys.argv[1]
    else:
        print "Error: No DQ2 container name given !"
        sys.exit(1)
    
    print "Quering DQ2 container: %s ..." %(containername)
    dq2 = DQ2()
    datasets = dq2.listDatasetsInContainer(containername)

    print "Container holds %s DQ2 dataset(s)" %(len(datasets))

    amidatasets = []
    for dataset in datasets:
        pos = dataset.find('_tid')
        amidatasets.append(dataset[:pos])
    
    uniqueamidatasets = set(amidatasets)
    print "This corresponds to %s logical AMI dataset(s)" %(len(uniqueamidatasets))

    try:
        amiclient=AMI()    
    except Exception, msg:
        print msg
        
    totalevents = 0

    for amidataset in uniqueamidatasets:

        try:
            amiCommand = []
            amiCommand.append("GetDatasetInfo")
            amiCommand.append("logicalDatasetName=" + amidataset)
            result=amiclient.execute(amiCommand)
            res = result.getDict()
        except Exception, msg:
            print msg
        events = int(res['Element_Info']['row_1']['totalEvents'])
        print 'AMIDataset: %s contains %s event(s)' %(amidataset, events )
        totalevents += events

    print 'Total: %s contains %s event(s)' %(containername, totalevents)

