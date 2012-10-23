#!/usr/bin/env  python

import sys
import os
from glob import glob

join = os.path.join
base = os.path.dirname(os.path.abspath(os.path.realpath(__file__)))
sys.path[0:0] = glob(join(base, 'eggs/*.egg'))
