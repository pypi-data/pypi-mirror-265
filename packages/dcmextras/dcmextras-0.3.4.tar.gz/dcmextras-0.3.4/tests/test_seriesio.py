#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import os
from os.path import dirname, abspath, join
import sys
import numpy as np
import math

from glob import glob

from zipfile import ZipFile
from tempfile import NamedTemporaryFile

from pydicom import dcmread

TESTDIR = dirname(abspath(__file__))
TESTDATA = join(TESTDIR, 'testdata')
sys.path.insert(0, abspath(join(TESTDIR, '..')))

from dcmextras import seriesio


class TestSeriesIOPCFlow(unittest.TestCase):
    ''' Tests for functions in seriesio.py '''

    def setUp(self):
        self.datadir = join(TESTDATA, 'pcflow-vb17')

        # an amplitude/phase pair
        self.amplimage = os.path.join(self.datadir, 'MR.0001.dcm')
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

    def test_read_series(self):
        # glob handling
        seriesa = seriesio.read_series(self.datadir)
        seriesb = seriesio.read_series(glob(os.path.join(self.datadir, '*.dcm')))
        assert len(seriesa) == len(seriesb) == len(glob(os.path.join(self.datadir, '*.dcm')))
        assert [img.SOPInstanceUID for img in seriesa] == [img.SOPInstanceUID for img in seriesb]

        # zipfile handling
        with NamedTemporaryFile(mode='w+b', suffix='.zip', delete=False) as tmpf:
            with ZipFile(tmpf, mode='w') as zipf:
                for fname in glob(os.path.join(self.datadir, '*.dcm')):
                    zipf.write(fname)
            zipname = tmpf.name

        seriesc = seriesio.read_series(zipname)
        assert sorted([img.SOPInstanceUID for img in seriesa]) == sorted([img.SOPInstanceUID for img in seriesc])
        os.unlink(zipname)

    def test_read_time_series(self):
        seriesa = seriesio.read_time_series(self.uniform)
        seriesb = seriesio.read_time_series(self.nonuniform)
        assert len(seriesa) == len(seriesb)

    def test_read_flow_series(self):
        seriesa, seriesb = seriesio.read_flow_series(self.datadir)
        assert len(seriesa) == len(seriesb)

    def test_series_as_array(self):
        nparray = seriesio.series_as_array(seriesio.read_series(self.uniform))
        assert nparray.shape == (4, 192, 256)
        assert nparray.dtype == np.int16
        assert nparray.flags['C_CONTIGUOUS']


class TestSeriesIOASL(unittest.TestCase):
    ''' Tests for functions in seriesio.py '''

    def setUp(self):
        self.datadir = join(TESTDATA, 'asl2d-vd11')

    def test_read_series(self):
        # glob handling
        seriesa = seriesio.read_series(self.datadir)
        seriesb = seriesio.read_series(glob(os.path.join(self.datadir, '*.dcm')))
        assert len(seriesa) == len(seriesb) == len(glob(os.path.join(self.datadir, '*.dcm')))
        assert [img.SOPInstanceUID for img in seriesa] == [img.SOPInstanceUID for img in seriesb]

        # zipfile handling
        with NamedTemporaryFile(mode='w+b', suffix='.zip', delete=False) as tmpf:
            with ZipFile(tmpf, mode='w') as zipf:
                for fname in glob(os.path.join(self.datadir, '*.dcm')):
                    zipf.write(fname)
            zipname = tmpf.name

        seriesc = seriesio.read_series(zipname)
        assert sorted([img.SOPInstanceUID for img in seriesa]) == sorted([img.SOPInstanceUID for img in seriesc])
        os.unlink(zipname)

    def test_read_time_series(self):
        seriesa = seriesio.read_time_series(self.datadir)
        # nb times should be increasing in ASL series, but probably not uniformly
        time_deltas = np.diff([float(d.AcquisitionTime) for d in seriesa])
        assert np.all(time_deltas > 0)

    def test_series_as_array(self):
        nparray = seriesio.series_as_array(seriesio.read_series(self.datadir))
        assert nparray.shape == (91, 192, 192)
        assert nparray.dtype == np.int16
        assert nparray.flags['C_CONTIGUOUS']

    def test_stack_from_mosaic_image(self):
        dobj = dcmread(glob(os.path.join(self.datadir, '*.dcm'))[0])
        _NumberOfImagesInMosaic = 0x0019, 0x100a
        nimages = int(dobj[_NumberOfImagesInMosaic].value)
        assert nimages > 1
        # number of images on a side
        ntiles = int(math.ceil(math.sqrt(nimages)))
        assert ntiles > 1
        nparray = seriesio.stack_from_mosaic_image(dobj)
        assert nparray.shape == (nimages, dobj.Rows//ntiles, dobj.Columns//ntiles)

    def test_stack_from_mosaic_time_series(self):
        seriesa = seriesio.read_time_series(self.datadir)
        _NumberOfImagesInMosaic = 0x0019, 0x100a
        nimages = int(seriesa[0][_NumberOfImagesInMosaic].value)
        assert nimages > 1
        # number of images on a side
        ntiles = int(math.ceil(math.sqrt(nimages)))
        assert ntiles > 1
        nparray, (dx, dy, dz, dt) = seriesio.stack_from_mosaic_time_series(seriesa)
        assert nparray.shape == (len(seriesa), nimages, seriesa[0].Rows // ntiles, seriesa[0].Columns // ntiles)
        assert dx, dy == seriesa[0].Pixelspacing
        assert dz == seriesa[0].SpacingBetweenSlices
        assert dt == float(seriesa[1].AcquisitionTime) - float(seriesa[0].AcquisitionTime)

    def test_stack_from_asl_mosaic_time_series(self):
        seriesa = seriesio.read_time_series(self.datadir)
        _NumberOfImagesInMosaic = 0x0019, 0x100a
        nimages = int(seriesa[0][_NumberOfImagesInMosaic].value)
        assert nimages > 1
        # number of images on a side
        ntiles = int(math.ceil(math.sqrt(nimages)))
        assert ntiles > 1
        nparray, (tr_ms, te_ms, slice_delays, qcdata) = seriesio.stack_from_asl_mosaic_time_series(seriesa)
        assert nparray.shape == (len(seriesa), nimages, seriesa[0].Rows // ntiles, seriesa[0].Columns // ntiles)
        assert len(slice_delays) == nimages
        time_deltas = np.diff(slice_delays)
        assert np.all(time_deltas > 0)
        assert np.allclose(time_deltas, time_deltas[0])
        assert (tr_ms, te_ms) == (2500, 12)
        assert (qcdata[3], qcdata[4]) == (700, 1800)


if __name__ == '__main__':
    unittest.main()
