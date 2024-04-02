#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
from os.path import dirname, abspath, join
import sys
import re

from pydicom import dcmread

TESTDIR = dirname(abspath(__file__))
TESTDATA = join(TESTDIR, 'testdata')
sys.path.insert(0, abspath(join(TESTDIR, '..')))

from dcmextras import siemensphoenix


class TestSiemensPhoenixVB17(unittest.TestCase):
    def setUp(self):
        self.filename = join(TESTDATA, 'pcflow-vb17/MR.0001.dcm')

    def test_raw_phoenix(self):
        dobj = dcmread(self.filename)
        phoenix = siemensphoenix.phoenix(dobj, raw=True)
        assert phoenix
        assert isinstance(phoenix, dict)
        self.assertEqual(phoenix['sPhysioImaging.lPhases'], 102)

        pattern = r'asCoilSelectMeas\[\d\]\.asList\[\d{1,2}\]\.sCoilElementID\.tCoilID'
        cids = [v for k, v in phoenix.items() if re.match(pattern, k)]
        assert cids
        self.assertEqual(max(set(cids), key=cids.count), 'SpineMatrix')

        self.assertEqual(float(phoenix['sGRADSPEC.flSensitivityX']) * 1e6, 78.5676)
        self.assertEqual(float(phoenix['sGRADSPEC.flSensitivityY']) * 1e6, 78.5165)
        self.assertEqual(float(phoenix['sGRADSPEC.flSensitivityZ']) * 1e6, 90.991)

    def test_cooked_phoenix(self):
        dobj = dcmread(self.filename)
        phoenix = siemensphoenix.phoenix(dobj, raw=False)
        assert phoenix
        assert isinstance(phoenix, dict)
        self.assertEqual(phoenix['PhysioImaging']['Phases'], 102)

        cids = [
            item['CoilElementID']['CoilID']
            for item in
            phoenix['CoilSelectMeas'][0]['List']
        ]
        assert cids
        self.assertEqual(max(set(cids), key=cids.count), 'SpineMatrix')

        self.assertEqual(float(phoenix['GRADSPEC']['SensitivityX']) * 1e6, 78.5676)
        self.assertEqual(float(phoenix['GRADSPEC']['SensitivityY']) * 1e6, 78.5165)
        self.assertEqual(float(phoenix['GRADSPEC']['SensitivityZ']) * 1e6, 90.991)


class TestSiemensPhoenixVB19(unittest.TestCase):
    def setUp(self):
        self.filename = join(TESTDATA, 'lge-vb19.dcm')

    def test_raw_phoenix(self):
        dobj = dcmread(self.filename)
        phoenix = siemensphoenix.phoenix(dobj, raw=True)
        assert phoenix
        assert isinstance(phoenix, dict)
        self.assertEqual(phoenix['sPhysioImaging.lPhases'], 1)

        pattern = r'asCoilSelectMeas\[\d\]\.asList\[\d{1,2}\]\.sCoilElementID\.tCoilID'
        cids = [v for k, v in phoenix.items() if re.match(pattern, k)]
        assert cids
        self.assertEqual(max(set(cids), key=cids.count), 'SpineMatrix')

        self.assertEqual(float(phoenix['sGRADSPEC.flSensitivityX']) * 1e6, 78.6019)
        self.assertEqual(float(phoenix['sGRADSPEC.flSensitivityY']) * 1e6, 78.4516)
        self.assertEqual(float(phoenix['sGRADSPEC.flSensitivityZ']) * 1e6, 91.0151)

    def test_cooked_phoenix(self):
        dobj = dcmread(self.filename)
        phoenix = siemensphoenix.phoenix(dobj, raw=False)
        assert phoenix
        assert isinstance(phoenix, dict)
        self.assertEqual(phoenix['PhysioImaging']['Phases'], 1)

        cids = [
            item['CoilElementID']['CoilID']
            for item in
            phoenix['CoilSelectMeas'][0]['List']
        ]
        assert cids
        self.assertEqual(max(set(cids), key=cids.count), 'SpineMatrix')

        self.assertEqual(float(phoenix['GRADSPEC']['SensitivityX']) * 1e6, 78.6019)
        self.assertEqual(float(phoenix['GRADSPEC']['SensitivityY']) * 1e6, 78.4516)
        self.assertEqual(float(phoenix['GRADSPEC']['SensitivityZ']) * 1e6, 91.0151)


class TestSiemensPhoenixVE11A(unittest.TestCase):
    def setUp(self):
        self.filename = join(TESTDATA, 'se-single-ve11a.dcm')

    def test_raw_phoenix(self):
        dobj = dcmread(self.filename)
        phoenix = siemensphoenix.phoenix(dobj, raw=True)
        assert phoenix
        assert isinstance(phoenix, dict)
        self.assertEqual(phoenix['sCoilSelectMeas.dOverallImageScaleCorrectionFactor'], 2.0)

        pattern = r'sCoilSelectMeas\.aRxCoilSelectData\[\d\]\.asList\[\d{1,2}\]\.sCoilElementID\.tCoilID'
        cids = [v for k, v in phoenix.items() if re.match(pattern, k)]
        assert cids
        self.assertEqual(max(set(cids), key=cids.count), 'Head_32')

        self.assertEqual(float(phoenix['sGRADSPEC.asGPAData[0].flSensitivityX']) * 1e6, 89.4815966603)
        self.assertEqual(float(phoenix['sGRADSPEC.asGPAData[0].flSensitivityY']) * 1e6, 89.0809023986)
        self.assertEqual(float(phoenix['sGRADSPEC.asGPAData[0].flSensitivityZ']) * 1e6, 89.18689854910001)

    def test_cooked_phoenix(self):
        dobj = dcmread(self.filename)
        phoenix = siemensphoenix.phoenix(dobj, raw=False)
        assert phoenix
        assert isinstance(phoenix, dict)
        self.assertEqual(phoenix['CoilSelectMeas']['OverallImageScaleCorrectionFactor'], 2.0)

        cids = [
            item['CoilElementID']['CoilID']
            for item in
            phoenix['CoilSelectMeas']['RxCoilSelectData'][0]['List']
        ]
        assert cids
        self.assertEqual(max(set(cids), key=cids.count), 'Head_32')

        self.assertEqual(float(phoenix['GRADSPEC']['GPAData'][0]['SensitivityX']) * 1e6, 89.4815966603)
        self.assertEqual(float(phoenix['GRADSPEC']['GPAData'][0]['SensitivityY']) * 1e6, 89.0809023986)
        self.assertEqual(float(phoenix['GRADSPEC']['GPAData'][0]['SensitivityZ']) * 1e6, 89.18689854910001)


class TestSiemensPhoenixXA11AEnhanced(unittest.TestCase):
    def setUp(self):
        self.filename = join(TESTDATA, 'se-enhanced-xa11a.dcm')

    def test_raw_phoenix(self):
        dobj = dcmread(self.filename)
        phoenix = siemensphoenix.phoenix(dobj, raw=True)
        assert phoenix
        assert isinstance(phoenix, dict)
        self.assertEqual(phoenix['sCoilSelectMeas.dOverallImageScaleCorrectionFactor'], 1.0)

        pattern = r'sCoilSelectMeas\.aRxCoilSelectData\[\d\]\.asList\[\d{1,2}\]\.sCoilElementID\.tCoilID'
        cids = [v for k, v in phoenix.items() if re.match(pattern, k)]
        assert cids
        self.assertEqual(max(set(cids), key=cids.count), 'HeadNeck_20_TCS')

        self.assertEqual(float(phoenix['sGRADSPEC.asGPAData[0].flSensitivityX']) * 1e6, 93.1628383114)
        self.assertEqual(float(phoenix['sGRADSPEC.asGPAData[0].flSensitivityY']) * 1e6, 93.9305391512)
        self.assertEqual(float(phoenix['sGRADSPEC.asGPAData[0].flSensitivityZ']) * 1e6, 91.8394216569)

    def test_cooked_phoenix(self):
        dobj = dcmread(self.filename)
        phoenix = siemensphoenix.phoenix(dobj, raw=False)
        assert phoenix
        assert isinstance(phoenix, dict)
        self.assertEqual(phoenix['CoilSelectMeas']['OverallImageScaleCorrectionFactor'], 1.0)

        cids = [
            item['CoilElementID']['CoilID']
            for item in
            phoenix['CoilSelectMeas']['RxCoilSelectData'][0]['List']
        ]
        assert cids
        self.assertEqual(max(set(cids), key=cids.count), 'HeadNeck_20_TCS')

        self.assertEqual(float(phoenix['GRADSPEC']['GPAData'][0]['SensitivityX']) * 1e6, 93.1628383114)
        self.assertEqual(float(phoenix['GRADSPEC']['GPAData'][0]['SensitivityY']) * 1e6, 93.9305391512)
        self.assertEqual(float(phoenix['GRADSPEC']['GPAData'][0]['SensitivityZ']) * 1e6, 91.8394216569)


class TestSiemensPhoenixXA11AInterop(unittest.TestCase):
    def setUp(self):
        self.filename = join(TESTDATA, 'se-interop-xa11a.dcm')

    def test_raw_phoenix(self):
        dobj = dcmread(self.filename)
        phoenix = siemensphoenix.phoenix(dobj, raw=True)
        assert phoenix
        assert isinstance(phoenix, dict)
        self.assertEqual(phoenix['sCoilSelectMeas.dOverallImageScaleCorrectionFactor'], 1.0)

        pattern = r'sCoilSelectMeas\.aRxCoilSelectData\[\d\]\.asList\[\d{1,2}\]\.sCoilElementID\.tCoilID'
        cids = [v for k, v in phoenix.items() if re.match(pattern, k)]
        assert cids
        self.assertEqual(max(set(cids), key=cids.count), 'HeadNeck_20_TCS')

        self.assertEqual(float(phoenix['sGRADSPEC.asGPAData[0].flSensitivityX']) * 1e6, 93.1628383114)
        self.assertEqual(float(phoenix['sGRADSPEC.asGPAData[0].flSensitivityY']) * 1e6, 93.9305391512)
        self.assertEqual(float(phoenix['sGRADSPEC.asGPAData[0].flSensitivityZ']) * 1e6, 91.8394216569)

    def test_cooked_phoenix(self):
        dobj = dcmread(self.filename)
        phoenix = siemensphoenix.phoenix(dobj, raw=False)
        assert phoenix
        assert isinstance(phoenix, dict)
        self.assertEqual(phoenix['CoilSelectMeas']['OverallImageScaleCorrectionFactor'], 1.0)

        cids = [
            item['CoilElementID']['CoilID']
            for item in
            phoenix['CoilSelectMeas']['RxCoilSelectData'][0]['List']
        ]
        assert cids
        self.assertEqual(max(set(cids), key=cids.count), 'HeadNeck_20_TCS')

        self.assertEqual(float(phoenix['GRADSPEC']['GPAData'][0]['SensitivityX']) * 1e6, 93.1628383114)
        self.assertEqual(float(phoenix['GRADSPEC']['GPAData'][0]['SensitivityY']) * 1e6, 93.9305391512)
        self.assertEqual(float(phoenix['GRADSPEC']['GPAData'][0]['SensitivityZ']) * 1e6, 91.8394216569)


if __name__ == '__main__':
    unittest.main()
