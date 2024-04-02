#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import os
from os.path import dirname, abspath, join
import sys

from pydicom import dcmread

TESTDIR = dirname(abspath(__file__))
TESTDATA = join(TESTDIR, 'testdata')
sys.path.insert(0, abspath(join(TESTDIR, '..')))

from dcmextras import siemensoog


class TestSiemensOOG1(unittest.TestCase):
    ''' Tests for functions in siemensoog.py '''

    def setUp(self):
        self.datadir = join(TESTDATA, 'pcflow-vb17')

        # an amplitude/phase pair
        self.amplimage  = os.path.join(self.datadir, 'MR.0001.dcm')
        self.phaseimage = os.path.join(self.datadir, 'MR.0002.dcm')

        # a graphics panel image
        self.csaimage = os.path.join(self.datadir, 'MR.0064.dcm')

        # a uniform series of slices
        self.uniform = [os.path.join(self.datadir, 'MR.0001.dcm'),
                        os.path.join(self.datadir, 'MR.0003.dcm'),
                        os.path.join(self.datadir, 'MR.0005.dcm'),
                        os.path.join(self.datadir, 'MR.0007.dcm')]

        # a series of slice with a missing slice
        self.nonuniform = [os.path.join(self.datadir, 'MR.0001.dcm'),
                           os.path.join(self.datadir, 'MR.0003.dcm'),
                           os.path.join(self.datadir, 'MR.0007.dcm'),
                           os.path.join(self.datadir, 'MR.0009.dcm')]

    def test_extract_contours(self):
        # check we get the expected contours on an amplitude image
        dobj = dcmread(self.amplimage)
        oog = siemensoog.SiemensOOG(dobj)
        structures = oog.extract_contours()
        self.assertEqual(sorted(k for k in structures), sorted(['ArgusFlow01', 'ArgusFlowContourRef']))

        # and they have the correct number of points
        contourpoints_a = structures['ArgusFlow01']['contour']
        self.assertEqual(len(contourpoints_a), 465)

        # get_structures should return 2D points even though Siemens points are 3D with Z=0
        self.assertEqual(len(contourpoints_a[0]), 2)

        # structures defined on amplitued and phase images are the same
        dobj = dcmread(self.phaseimage)
        oog = siemensoog.SiemensOOG(dobj)
        structures = oog.extract_contours()
        contourpoints_p = structures['ArgusFlow01']['contour']
        self.assertEqual(contourpoints_p, contourpoints_a)


if __name__ == '__main__':
    unittest.main()
