#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import sys
import os
from os.path import dirname, abspath, join

from io import BytesIO
import warnings

from pydicom import dcmread

TESTDIR = dirname(abspath(__file__))
TESTDATA = join(TESTDIR, 'testdata')
sys.path.insert(0, abspath(join(TESTDIR, '..')))

from dcmextras import siemenscsa


class TestSiemensCSAVB17Flow(unittest.TestCase):
    ''' Tests for functions in siemenscsa.py using a flow series'''

    def setUp(self):
        self.datadir = join(TESTDATA, 'pcflow-vb17')

        # an amplitude/phase pair
        self.amplimage = os.path.join(self.datadir, 'MR.0001.dcm')
        self.phaseimage = os.path.join(self.datadir, 'MR.0002.dcm')

        # a graphics panel image
        self.csaimage = os.path.join(self.datadir, 'MR.0064.dcm')

        # a uniform series of slices
        self.uniform = [
            os.path.join(self.datadir, 'MR.0001.dcm'),
            os.path.join(self.datadir, 'MR.0003.dcm'),
            os.path.join(self.datadir, 'MR.0005.dcm'),
            os.path.join(self.datadir, 'MR.0007.dcm')
        ]

        # a series of slice with a missing slice
        self.nonuniform = [
            os.path.join(self.datadir, 'MR.0001.dcm'),
            os.path.join(self.datadir, 'MR.0003.dcm'),
            os.path.join(self.datadir, 'MR.0007.dcm'),
            os.path.join(self.datadir, 'MR.0009.dcm')
        ]

    def test_extract_csa_image_tags(self):
        # check we get the expected tags
        magn = dcmread(self.amplimage)
        magncsa = siemenscsa.csa(magn, 'Image')
        self.assertTrue(isinstance(magncsa, dict))
        self.assertTrue('FlowVenc' in magncsa)
        # arguably this should be a NaN when float tag is present but empty
        self.assertEqual(magncsa['FlowVenc'], '')

        phse = dcmread(self.phaseimage)
        phsecsa = siemenscsa.csa(phse, 'Image')
        self.assertTrue(isinstance(phsecsa, dict))
        self.assertTrue('FlowVenc' in phsecsa)
        self.assertTrue(isinstance(phsecsa['FlowVenc'], float))
        self.assertEqual(phsecsa['FlowVenc'], 250.0)

        grph = dcmread(self.csaimage)
        self.assertRaises(AttributeError, siemenscsa.csa, grph, 'Image')

    def test_extract_csa_series_tags(self):
        # check we get the expected tags
        magn = dcmread(self.amplimage)
        magncsa = siemenscsa.csa(magn, 'Series')
        self.assertTrue(isinstance(magncsa, dict))
        self.assertTrue('FlowVenc' not in magncsa)

        phse = dcmread(self.phaseimage)
        phsecsa = siemenscsa.csa(phse, 'Series')
        self.assertTrue(isinstance(phsecsa, dict))
        self.assertTrue('FlowVenc' not in phsecsa)

        grph = dcmread(self.csaimage)
        grphcsa = siemenscsa.csa(grph, 'Series')
        self.assertTrue(isinstance(grphcsa, dict))
        self.assertTrue('FlowVenc' not in phsecsa)

        self.assertTrue(grphcsa == phsecsa == magncsa)

    def test_extract_phoenix_protocol(self):
        magn = dcmread(self.amplimage)
        phse = dcmread(self.phaseimage)
        grph = dcmread(self.csaimage)

        magnphoenix = siemenscsa.phoenix(magn)
        phsephoenix = siemenscsa.phoenix(phse)
        grphphoenix = siemenscsa.phoenix(grph)

        self.assertTrue(isinstance(magnphoenix, dict))
        self.assertTrue(grphphoenix == phsephoenix == magnphoenix)
        self.assertTrue(magnphoenix['sProtConsistencyInfo.tBaselineString'] == 'N4_VB17A_LATEST_20090307')
        self.assertTrue(magnphoenix['asCoilSelectMeas[0].tNucleus'] == '1H')


class TestSiemensCSAVD11Bold(unittest.TestCase):
    ''' Tests for functions in siemenscsa.py using a vd11 bold frame'''

    def setUp(self):
        self.boldmosaic = join(TESTDATA, 'vd11-ep2d.dcm')

    def test_extract_csa_tags(self):
        mosaic = dcmread(self.boldmosaic)
        csa_default = siemenscsa.csa(mosaic)
        csa_series = siemenscsa.csa(mosaic, 'Series')
        csa_image = siemenscsa.csa(mosaic, 'Image')

        self.assertTrue(isinstance(csa_default, dict))
        self.assertTrue(csa_default == csa_series)
        self.assertTrue(csa_default != csa_image)

    def test_extract_phoenix_protocol(self):
        mosaic = dcmread(self.boldmosaic)
        phoenix = siemenscsa.phoenix(mosaic)

        self.assertTrue(isinstance(phoenix, dict))
        self.assertTrue(phoenix['sProtConsistencyInfo.tBaselineString'] == 'N4_VD11D_LATEST_20110129')
        self.assertTrue(phoenix['sCoilSelectMeas.aRxCoilSelectData[0].tNucleus'] == '1H')


class TestSiemensCSAVD11Bold(unittest.TestCase):
    ''' Tests for functions in siemenscsa.py using a vd11 bold frame'''

    def setUp(self):
        self.boldframe = join(TESTDATA, 'vd11-ep2d.dcm')

    def test_extract_csa_tags(self):
        mosaic = dcmread(self.boldframe)
        csa_default = siemenscsa.csa(mosaic)
        csa_series = siemenscsa.csa(mosaic, 'Series')
        csa_image = siemenscsa.csa(mosaic, 'Image')

        self.assertTrue(isinstance(csa_default, dict))
        self.assertTrue(csa_default == csa_series)
        self.assertTrue(csa_default != csa_image)

    def test_extract_phoenix_protocol(self):
        mosaic = dcmread(self.boldframe)
        phoenix = siemenscsa.phoenix(mosaic)

        self.assertTrue(isinstance(phoenix, dict))
        self.assertTrue(phoenix['sProtConsistencyInfo.tBaselineString'] == 'N4_VD11D_LATEST_20110129')
        self.assertTrue(phoenix['sCoilSelectMeas.aRxCoilSelectData[0].tNucleus'] == '1H')


class TestSiemensCSAVD11Asl(unittest.TestCase):
    ''' Tests for functions in siemenscsa.py using a vd11 asl frame'''

    def setUp(self):
        self.aslframe = join(TESTDATA, 'asl2d-vd11', '025AC78B.dcm')
        self.mosaic = dcmread(self.aslframe)

    def test_extract_csa_tags(self):
        csa_default = siemenscsa.csa(self.mosaic)
        csa_series = siemenscsa.csa(self.mosaic, 'Series')
        csa_image = siemenscsa.csa(self.mosaic, 'Image')

        self.assertTrue(isinstance(csa_default, dict))
        self.assertTrue(csa_default == csa_series)
        self.assertTrue(csa_default != csa_image)

    def test_extract_phoenix_protocol(self):
        phoenix = siemenscsa.phoenix(self.mosaic)
        self.assertTrue(isinstance(phoenix, dict))
        self.assertTrue(phoenix['sProtConsistencyInfo.tBaselineString'] == 'N4_VD11D_LATEST_20110105')
        self.assertTrue(phoenix['sCoilSelectMeas.aRxCoilSelectData[0].tNucleus'] == '1H')

    def test_csa_tags_against_nibabel(self):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            import nibabel.nicom.csareader as csareader

        def trim_list(lst):
            '''
            Remove trailing empty strings from list
            '''
            try:
                i = [bool(s.decode('ascii')) if isinstance(s, bytes) else bool(str(s)) for s in reversed(lst)].index(True)
            except ValueError:
                return lst
            return lst[:-i] if i > 0 else lst

        csa_series = siemenscsa.csa(self.mosaic, 'Series')
        csa_image = siemenscsa.csa(self.mosaic, 'Image')
        csa_series_nibabel = csareader.get_csa_header(self.mosaic, csa_type='series')
        csa_image_nibabel = csareader.get_csa_header(self.mosaic, csa_type='image')

        for t in csa_image:
            if t in csa_image_nibabel['tags']:
                if isinstance(csa_image[t], (list, tuple)):
                    if (t, csa_image[t]) != (t, trim_list(csa_image_nibabel['tags'][t]['items'])):
                        print(csa_image_nibabel['tags'][t]['items'])
                    self.assertEqual((t, csa_image[t]), (t, trim_list(csa_image_nibabel['tags'][t]['items'])))
                elif len(csa_image_nibabel['tags'][t]['items']) > 0:
                    self.assertEqual((t, csa_image[t]), (t, csa_image_nibabel['tags'][t]['items'][0]))
                else:
                    self.assertEqual((t, csa_image[t]), (t, ''))

        for t in set(csa_series.keys()) - set(['MrPhoenixProtocol']):
            if t in csa_series_nibabel['tags']:
                if isinstance(csa_series[t], (list, tuple)):
                    self.assertEqual((t, csa_series[t]), (t, trim_list(csa_series_nibabel['tags'][t]['items'])))
                elif len(csa_series_nibabel['tags'][t]['items']) > 0:
                    self.assertEqual((t, csa_series[t]), (t, csa_series_nibabel['tags'][t]['items'][0]))
                else:
                    self.assertEqual((t, csa_series[t]), (t, ''))

        # Check lines individually in MrPhoenixProtocol
        linesa = csa_series['MrPhoenixProtocol'].splitlines()
        linesb = csa_series_nibabel['tags']['MrPhoenixProtocol']['items'][0].splitlines()
        for linea, lineb in zip(linesa, linesb):
            self.assertEqual(linea, lineb)

    def test_read_header(self):
        CSAImageHeaderInfo = (0x0029, 0x1010)
        ntags = siemenscsa.read_header(BytesIO(self.mosaic[CSAImageHeaderInfo].value))
        self.assertEqual(ntags, 93)
        CSASeriesHeaderInfo = (0x0029, 0x1020)
        ntags = siemenscsa.read_header(BytesIO(self.mosaic[CSASeriesHeaderInfo].value))
        self.assertEqual(ntags, 74)

    def test_read_tag(self):
        CSAImageHeaderInfo = (0x0029, 0x1010)
        f = BytesIO(self.mosaic[CSAImageHeaderInfo].value)
        ntags = siemenscsa.read_header(f)
        tags = [siemenscsa.read_tag(f) for i in range(ntags)]
        tags_processed = siemenscsa.map_vrs(tags)


class TestSiemensCSAVD13FID(unittest.TestCase):
    ''' Tests for functions in siemenscsa.py using a vd13 fid object'''

    def setUp(self):
        self.fidfile = join(TESTDATA, 'fid-vd13.dcm')
        self.fidobj = dcmread(self.fidfile)

    def test_extract_csa_tags(self):
        csa_default = siemenscsa.csa(self.fidobj)
        csa_series = siemenscsa.csa(self.fidobj, 'Series')
        csa_image = siemenscsa.csa(self.fidobj, 'Image')

        self.assertTrue(isinstance(csa_default, dict))
        self.assertTrue(csa_default == csa_series)
        self.assertTrue(csa_default != csa_image)

    def test_extract_phoenix_protocol(self):
        phoenix = siemenscsa.phoenix(self.fidobj)
        self.assertTrue(isinstance(phoenix, dict))
        self.assertTrue(phoenix['sProtConsistencyInfo.tBaselineString'] == 'N4_VD13C_LATEST_20121117')
        self.assertTrue(phoenix['sCoilSelectMeas.aRxCoilSelectData[0].tNucleus'] == '1H')

    def test_csa_tags_against_nibabel(self):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            import nibabel.nicom.csareader as csareader

        def trim_list(lst):
            '''
            Remove trailing empty strings from list
            '''
            try:
                i = [bool(s.decode('ascii')) if isinstance(s, bytes) else bool(str(s)) for s in reversed(lst)].index(True)
            except ValueError:
                return lst
            return lst[:-i] if i > 0 else lst

        csa_series = siemenscsa.csa(self.fidobj, 'Series')
        csa_image = siemenscsa.csa(self.fidobj, 'Image')
        csa_series_nibabel = csareader.get_csa_header(self.fidobj, csa_type='series')
        csa_image_nibabel = csareader.get_csa_header(self.fidobj, csa_type='image')

        for t in csa_image:
            if t in csa_image_nibabel['tags']:
                if isinstance(csa_image[t], (list, tuple)):
                    if (t, csa_image[t]) != (t, trim_list(csa_image_nibabel['tags'][t]['items'])):
                        print(csa_image_nibabel['tags'][t]['items'])
                    self.assertEqual((t, csa_image[t]), (t, trim_list(csa_image_nibabel['tags'][t]['items'])))
                elif len(csa_image_nibabel['tags'][t]['items']) > 0:
                    self.assertEqual((t, csa_image[t]), (t, csa_image_nibabel['tags'][t]['items'][0]))
                else:
                    self.assertEqual((t, csa_image[t]), (t, ''))

        for t in set(csa_series.keys()) - set(['MrPhoenixProtocol']):
            if t in csa_series_nibabel['tags']:
                if isinstance(csa_series[t], (list, tuple)):
                    self.assertEqual((t, csa_series[t]), (t, trim_list(csa_series_nibabel['tags'][t]['items'])))
                elif len(csa_series_nibabel['tags'][t]['items']) > 0:
                    self.assertEqual((t, csa_series[t]), (t, csa_series_nibabel['tags'][t]['items'][0]))
                else:
                    self.assertEqual((t, csa_series[t]), (t, ''))

        # Check lines individually in MrPhoenixProtocol
        linesa = csa_series['MrPhoenixProtocol'].splitlines()
        linesb = csa_series_nibabel['tags']['MrPhoenixProtocol']['items'][0].splitlines()
        for linea, lineb in zip(linesa, linesb):
            self.assertEqual(linea, lineb)

    def test_read_header(self):
        CSAImageHeaderInfo = (0x0029, 0x1110)
        ntags = siemenscsa.read_header(BytesIO(self.fidobj[CSAImageHeaderInfo].value))
        self.assertEqual(ntags, 85)
        CSASeriesHeaderInfo = (0x0029, 0x1120)
        ntags = siemenscsa.read_header(BytesIO(self.fidobj[CSASeriesHeaderInfo].value))
        self.assertEqual(ntags, 75)

    def test_read_tag(self):
        CSAImageHeaderInfo = (0x0029, 0x1110)
        f = BytesIO(self.fidobj[CSAImageHeaderInfo].value)
        ntags = siemenscsa.read_header(f)
        tags = [siemenscsa.read_tag(f) for i in range(ntags)]
        tags_processed = siemenscsa.map_vrs(tags)


class TestSiemensCSAVE11Single(unittest.TestCase):
    ''' Tests for functions in siemenscsa.py using a ve11 single coil element image'''

    def setUp(self):
        self.sefile = join(TESTDATA, 'se-single-ve11a.dcm')
        self.dobj = dcmread(self.sefile)

    def test_extract_csa_tags(self):
        csa_default = siemenscsa.csa(self.dobj)
        csa_series = siemenscsa.csa(self.dobj, 'Series')
        csa_image = siemenscsa.csa(self.dobj, 'Image')

        self.assertTrue(isinstance(csa_default, dict))
        self.assertTrue(csa_default == csa_series)
        self.assertTrue(csa_default != csa_image)

        # coil channel
        self.assertEqual(csa_image['UsedChannelString'].index('X'), 0)

    def test_extract_phoenix_protocol(self):
        phoenix = siemenscsa.phoenix(self.dobj)
        self.assertTrue(isinstance(phoenix, dict))
        self.assertTrue(phoenix['sProtConsistencyInfo.tBaselineString'] == 'N4_VE11A_LATEST_20140830')
        self.assertTrue(phoenix['sCoilSelectMeas.aRxCoilSelectData[0].tNucleus'] == '1H')

    def test_csa_tags_against_nibabel(self):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            import nibabel.nicom.csareader as csareader

        def trim_list(lst):
            '''
            Remove trailing empty strings from list
            '''
            try:
                i = [bool(s.decode('ascii')) if isinstance(s, bytes) else bool(str(s)) for s in reversed(lst)].index(True)
            except ValueError:
                return lst
            return lst[:-i] if i > 0 else lst

        csa_series = siemenscsa.csa(self.dobj, 'Series')
        csa_image = siemenscsa.csa(self.dobj, 'Image')
        csa_series_nibabel = csareader.get_csa_header(self.dobj, csa_type='series')
        csa_image_nibabel = csareader.get_csa_header(self.dobj, csa_type='image')

        for t in csa_image:
            if t in csa_image_nibabel['tags']:
                if isinstance(csa_image[t], (list, tuple)):
                    if (t, csa_image[t]) != (t, trim_list(csa_image_nibabel['tags'][t]['items'])):
                        print(csa_image_nibabel['tags'][t]['items'])
                    self.assertEqual((t, csa_image[t]), (t, trim_list(csa_image_nibabel['tags'][t]['items'])))
                elif len(csa_image_nibabel['tags'][t]['items']) > 0:
                    self.assertEqual((t, csa_image[t]), (t, csa_image_nibabel['tags'][t]['items'][0]))
                else:
                    self.assertEqual((t, csa_image[t]), (t, ''))

        for t in set(csa_series.keys()) - set(['MrPhoenixProtocol']):
            if t in csa_series_nibabel['tags']:
                if isinstance(csa_series[t], (list, tuple)):
                    self.assertEqual((t, csa_series[t]), (t, trim_list(csa_series_nibabel['tags'][t]['items'])))
                elif len(csa_series_nibabel['tags'][t]['items']) > 0:
                    self.assertEqual((t, csa_series[t]), (t, csa_series_nibabel['tags'][t]['items'][0]))
                else:
                    self.assertEqual((t, csa_series[t]), (t, ''))

        # Check lines individually in MrPhoenixProtocol
        linesa = csa_series['MrPhoenixProtocol'].splitlines()
        linesb = csa_series_nibabel['tags']['MrPhoenixProtocol']['items'][0].splitlines()
        for linea, lineb in zip(linesa, linesb):
            self.assertEqual(linea, lineb)

    def test_read_header(self):
        CSAImageHeaderInfo = (0x0029, 0x1110)
        ntags = siemenscsa.read_header(BytesIO(self.dobj[CSAImageHeaderInfo].value))
        self.assertEqual(ntags, 101)
        CSASeriesHeaderInfo = (0x0029, 0x1120)
        ntags = siemenscsa.read_header(BytesIO(self.dobj[CSASeriesHeaderInfo].value))
        self.assertEqual(ntags, 79)

    def test_read_tag(self):
        CSAImageHeaderInfo = (0x0029, 0x1110)
        f = BytesIO(self.dobj[CSAImageHeaderInfo].value)
        ntags = siemenscsa.read_header(f)
        tags = [siemenscsa.read_tag(f) for i in range(ntags)]
        tags_processed = siemenscsa.map_vrs(tags)


if __name__ == '__main__':
    unittest.main()
