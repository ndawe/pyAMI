from pyAMI.client import AMIClient
from pyAMI.query import get_dataset_xsec_effic

client = AMIClient()

dataset = 'mc11_7TeV.125206.PowHegPythia_VBFH130_tautauhh.merge.NTUP_TAUMEDIUM.e893_s1310_s1300_r2730_r2780_p795'
xsec, effic = get_dataset_xsec_effic(client, dataset)
print 'xsec: %.5E nb' % xsec
print 'effic: %.2f' % effic
