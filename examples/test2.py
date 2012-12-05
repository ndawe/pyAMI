
try:
   import setup_pyAMI # this line needed to ensure correct python environment since pyAMI 4.0.3
except Exception :
   print("Exception")
from pyAMI.query import get_dataset_xsec_effic
from pyAMI.client import AMIClient
client = AMIClient()
dataset = 'mc11_7TeV.125206.PowHegPythia_VBFH130_tautauhh.evgen.EVNT.e893'
xsec, effic = get_dataset_xsec_effic(client, dataset)
print (str(xsec))  