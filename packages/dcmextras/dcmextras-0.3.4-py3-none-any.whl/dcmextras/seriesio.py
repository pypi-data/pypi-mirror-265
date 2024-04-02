#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math
from glob import glob
from os.path import isdir, isfile, exists, join
from zipfile import ZipFile, is_zipfile
from io import BytesIO
from operator import attrgetter
from collections.abc import Sequence, Callable

import numpy as np
from pydicom import dcmread

try:
    from . siemenscsa import csa
except (ImportError, ValueError, SystemError):
    # for testing
    from siemenscsa import csa


class DicomIOError(IOError):
    pass


def read_series(fileordirname, key=None, numeric=False, reverse=False, globspec='*.dcm'):
    '''
    Read a DICOM series from a directory or a zip file of DICOM files, optionally sorting the series.

    Parameters
    ----------
    fileordirname:
        A list of files, the name of directory containing dicom files, a zip file or a single dicom file.
    key:
        Sort key - either a unary function, a dicom tagname or a list of tag names.
    numeric:
        Sort keys numerically (if a DICOM Tag Name)
    reverse:
        Whether to reverse the direction of sorting
    globspec:
        Glob specification (or list of specs) to match files to read. It is ignored in the case of a zip file

    Returns
    -------
    out:
        List of dicom objects.
    '''
    if not isinstance(fileordirname, str):
        # Assume a sequence is just a list of simple filenames
        dobjs = [dcmread(fname) for fname in sorted(set(fileordirname))]
    elif isdir(fileordirname):
        # A directory name
        if isinstance(globspec, str):
            # General case is a list of globspecs
            globspec = [globspec]
        # NB: set() takes account of duplicate matches for multiple glob patterns
        files = sorted(set([f for pattern in globspec for f in glob(join(fileordirname, pattern))]))
        dobjs = [dcmread(fname) for fname in files]
    elif is_zipfile(fileordirname):
        with ZipFile(fileordirname) as zf:
            # Unfortunately, the filelike object returned by ZipFile.open()
            # does not provide tell(), which is needed by dcmread()
            # so we have to go via a BytesIO buffer.
            dobjs = []
            for finfo in zf.infolist():
                with BytesIO(zf.read(finfo)) as sio:
                    dobjs.append(dcmread(sio))

    elif isfile(fileordirname):
        # Degenerate case - single time point
        dobjs = [dcmread(fileordirname)]
    elif not exists(fileordirname):
        raise IOError("Specified file or directory '%s' does not exist" % fileordirname)
    else:
        raise IOError("%s' is neither a list of files, nor a directory, nor a zip file nor yet a plain file" % fileordirname)

    if key is not None:
        if isinstance(key, Callable):
            dobjs.sort(key=key, reverse=reverse)
        elif isinstance(key, str):
            if numeric:
                dobjs.sort(key=lambda d: float(getattr(d, key)), reverse=reverse)
            else:
                dobjs.sort(key=attrgetter(key), reverse=reverse)
        elif isinstance(key, Sequence) and all([isinstance(x, str) for x in key]):
            dobjs.sort(key=attrgetter(*key), reverse=reverse)
        else:
            raise TypeError('Sort key %s should be a string, a sequence of strings or a callable' % str(key))

    return dobjs


def read_time_series(fileordirname, key='AcquisitionTime', numeric=True, globspec='*.dcm'):
    '''
    Read a simple series from a directory or a zip file of DICOM files.
    The frames are sorted on in time using the 'AcquisitionTime' field.

    Parameters
    ----------
    fileordirname:
        Name of directory containing dicom files, a zip file or a single dicom file.
    key:
        Sort key - by default on acquisition time
    numeric:
        Sort keys numerically
    globspec:
        Glob specification (or list of specs) to match files to read. It is ignored in the case of a zip file

    Returns
    -------
    out:
        List of dicom objects..
    '''
    return read_series(fileordirname, key=key, reverse=False, numeric=numeric, globspec=globspec)


def read_flow_series(fileordirname, globspec='*.dcm'):
    '''
    Read a gated phase contrast flow series from a directory or a zip file of DICOM files.
    The frames are sorted on cardiac phase using the 'TriggerTime' field. The series are
    checked for spatial consistency and homogeneity of trigger time intervals.

    Parameters
    ----------
    fileordirname:
        Name of directory containing dicom files, a zip file or a single dicom file.
    globspec:
        Glob specification (or list of specs) to match files to read. It is ignored in the case of a zip file

    Returns
    -------
    magnitude_series, phase_series:
        Separate DICOM series for magnitude and phase data.
    '''

    series = read_series(fileordirname, 'InstanceNumber', reverse=False, numeric=True, globspec=globspec)
    if not series:
        raise DicomIOError('Unable to read series from %s' % fileordirname)

    # Separate out into magnitude and phase images, ignoring non flow objects and sort on trigger time
    magnitude_series = sorted([d for d in series if 'TriggerTime' in d and d.ImageType[2] == 'M'], key=lambda d: d.TriggerTime)
    phase_series = sorted([d for d in series if 'TriggerTime' in d and d.ImageType[2] == 'P'], key=lambda d: d.TriggerTime)

    if not magnitude_series or not phase_series:
        raise DicomIOError('Series (of %d images) does not appear to be a flow series' % len(series))

    if len(magnitude_series) != len(phase_series):
        raise DicomIOError('Different numbers of magnitude and phase images (%d, %d)' % (len(magnitude_series), len(phase_series)))

    position = magnitude_series[0].ImagePositionPatient
    if not all(d.ImagePositionPatient == position for d in magnitude_series + phase_series):
        raise DicomIOError('Flow images not all at the same slice location')

    if not all(a.TriggerTime == b.TriggerTime for (a, b) in zip(magnitude_series, phase_series)):
        raise DicomIOError('Trigger times on phase and magnitude images do not correspond')

    ts = [d.TriggerTime for d in phase_series]
    dts = [tb - ta for (ta, tb) in zip(ts[:-1], ts[1:])]
    ddts = [dtb - dta for (dta, dtb) in zip(dts[:-1], dts[1:])]
    if not all([math.fabs(ddt) < 0.01 for ddt in ddts]):
        raise DicomIOError('Trigger times unevenly spaced')

    return magnitude_series, phase_series


def series_as_array(dcmseries):
    '''
    Extract a rank 3 signed 16 bit numpy array with the 2D image data of a series.

    Parameters
    ----------
    dcmseries:
        A list of DICOM objects (assumed sorted appropriately).

    Returns
    -------
    nparray:
        An int16 Numpy array in 'C' order with image axes arranged (t, y, x)
    '''

    nx = dcmseries[0].Columns
    ny = dcmseries[0].Rows
    nt = len(dcmseries)
    nparray = np.empty((nt, ny, nx), np.int16, 'C')
    for t, d in enumerate(dcmseries):
        nparray[t, :, :] = d.pixel_array
    return nparray


def stack_from_mosaic_image(dcmobj, nimages=None):
    '''
    Extract a stack of images from a mosaic dicom object
    Returns a rank 3 numpy array organized nz,ny,nx

    Parameters
    ----------
    dcmobj :
        A mosaic pydicom dicom object.
    nimages :
        Number of images expected in mosaic. Default is to get this from Siemens private tag.
    '''

    if nimages is None:
        # Siemens Private Tag
        _NumberOfImagesInMosaic = 0x0019, 0x100a
        nimages = int(dcmobj[_NumberOfImagesInMosaic].value)

    # get dcm image data as numpy array
    mosaic = dcmobj.pixel_array

    # deduce number of tiles and image size in mosaic from number of images
    # assumes mosaic is always 'square'
    ntiles = int(math.ceil(math.sqrt(nimages)))
    ny, nx = mosaic.shape[0]//ntiles, mosaic.shape[1]//ntiles

    # unpack into a 3d volume (nz, ny, nx)
    stack = np.zeros([nimages, ny, nx])
    for i in range(nimages):
        x0 = (i % ntiles) * nx
        y0 = (i // ntiles) * ny
        stack[i] = mosaic[y0:y0+ny, x0:x0+nx]

    return stack


def stack_from_mosaic_time_series(dobjs):
    '''
    Extract a 4d numpy array from a list of dicom objects corresponding
    to a time series. Each object is expected to be one time point
    Returns a rank 4 numpy array organized nt,nz,ny,nx

    Parameters
    ----------
    dobjs :
        Dicom object list (assumed presorted in time order).
    '''
    # Pixel and slice spacing
    dx, dy = dobjs[0].PixelSpacing
    dz = dobjs[0].SpacingBetweenSlices

    # Temporal spacing
    acq_times = [float(d.AcquisitionTime) for d in dobjs]
    dt = acq_times[1] - acq_times[0]

    # Expand out the mosaics
    stacks = [stack_from_mosaic_image(dobj) for dobj in dobjs]

    # Return as a 4d numpy array (t, z, y, x)
    return (np.array(stacks), (dx, dy, dz, dt))


def stack_from_asl_mosaic_time_series(dobjs):
    '''
    Read an asl time series in mosaic form from specified dicom objects.
    Each object is expected to be one time point but this may be
      an M0 image (the 1st time point) or alternating tag/control (2nd, 3rd etc)
    Returns a rank 4 numpy array organized nt,nz,ny,nx the relative delays
      in the acquisition of the slices in the mosaic and sequence parameters
      including the TI times.

    Parameters
    ----------
    dobjs :
        Dicom object list (presorted in time order).
    '''

    # Siemens Private Tags
    _MosaicRefAcqTimes = 0x0019, 0x1029
    _TimeAfterStart = 0x0019, 0x1016

    if 'ASL' not in dobjs[0].ImageType:
        raise ValueError("Image is not an ASL one")
    if 'MOSAIC' not in dobjs[0].ImageType:
        raise ValueError("Image is not a Siemens Mosaic")

    if dobjs[0].MRAcquisitionType == '2D':
        # Sort the list of dicom objects on time after start
        dobjs = sorted(dobjs, key=lambda d: float(d[_TimeAfterStart].value))
        # check alternative sorting fields give the same ordering
        assert dobjs == sorted(dobjs, key=lambda d: d.AcquisitionTime)
        assert dobjs == sorted(dobjs, key=lambda d: d.InstanceNumber)
        assert dobjs == sorted(dobjs, key=lambda d: d.AcquisitionNumber)
    elif dobjs[0].MRAcquisitionType == '3D':
        # Sort the list of dicom objects on acquistion time
        dobjs = sorted(dobjs, key=lambda d: d.AcquisitionTime)
        # check alternative sorting fields give the same ordering
        assert dobjs == sorted(dobjs, key=lambda d: d.InstanceNumber)
        assert dobjs == sorted(dobjs, key=lambda d: d.AcquisitionNumber)
    else:
        raise ValueError("Unknown Sequence Type %s" % dobjs[0].MRAcquisitionType)

    # Expand out the mosaics, using 1st object to get no. of slices in mosaic
    stacks = [stack_from_mosaic_image(dobj) for dobj in dobjs]

    # Use first object as representative for the slice delays
    slice_delays = np.array(tuple(dobjs[0][_MosaicRefAcqTimes]))

    # Sequence parameters TI1, TI2 only seem to be available in csa header
    # These are in units of millisecs at indices 3 and 4 in 'QCData'
    qcdata = csa(dobjs[0], section='Image')['QCData']

    # Both in milliseconds
    tr_ms = dobjs[0].RepetitionTime
    te_ms = dobjs[0].EchoTime

    # Return image data as a 4d numpy array (t, z, y, x) along with some sequence params
    return np.array(stacks), (tr_ms, te_ms, slice_delays, qcdata)
