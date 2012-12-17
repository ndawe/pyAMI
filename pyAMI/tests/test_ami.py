#!/usr/bin/env python

import os
from pyAMI.client import AMIClient
from pyAMI.query import *
from unittest import TestCase
from nose.tools import assert_raises


class TestAMI(TestCase):

    client = None

    @classmethod
    def setup_class(cls):

        cls.client = AMIClient()

    def test_get_runs(self):

        runs = get_runs(self.client, periods=['B', 'K2'], year=11)

    def test_get_periods_for_run(self):

        periods = get_periods_for_run(self.client, 201351)

    def test_get_dataset_xsec_effic(self):

        dataset = 'mc11_7TeV.125206.PowHegPythia_VBFH130_tautauhh.evgen.EVNT.e893'
        xsec, effic = get_dataset_xsec_effic(self.client, dataset)


if __name__ == '__main__':
    import nose
    nose.runmodule()
