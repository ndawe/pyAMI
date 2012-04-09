"""
This module contains all default values

TODO: override with ami.cfg
"""

import datetime

# delay by half a year
YEAR = (datetime.date.today() - datetime.timedelta(182.5)).year % 1000
PROJECT = 'data%d_7TeV' % YEAR
STREAM = 'physics_JetTauEtmiss'
TYPE = 'AOD'
PRODSTEP = 'merge'
