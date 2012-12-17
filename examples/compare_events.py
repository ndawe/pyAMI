from pyAMI.client import AMIClient
from pyAMI.query import get_datasets, get_provenance, get_dataset_info

client = AMIClient()

ntup_tau = get_datasets(client, 'p1130', type='NTUP_TAU',
        parent_type='AOD', fields='events', flatten=True)

for nevents, ds in ntup_tau:
    print "checking %s ..." % ds
    print "%s events in NTUP_TAU" % nevents
    aod = get_provenance(client, ds, type='AOD').values()[0][0]
    aod_events = get_dataset_info(client, aod).info['totalEvents']
    print "checking %s ..." % aod
    print "%s events in AOD" % aod_events
    if int(aod_events) != int(nevents):
        print "MISMATCH!"
    print '-' * 20
