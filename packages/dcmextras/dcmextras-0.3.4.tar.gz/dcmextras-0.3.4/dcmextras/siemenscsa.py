#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Tools for extracting information from Siemens DICOM (CSA).

These include access to the CSA hidden tags and the Phoenix protocol tags.
"""

from struct import Struct
from warnings import warn
from io import BytesIO

from pydicom import dcmread

__all__ = ['csa', 'phoenix']

# The CSA tags we know about
_known_csa_tags = [
    "UsedPatientWeight",
    "NumberOfPrescans",
    "TransmitterCalibration",
    "PhaseGradientAmplitude",
    "ReadoutGradientAmplitude",
    "SelectionGradientAmplitude",
    "GradientDelayTime",
    "RfWatchdogMask",
    "RfPowerErrorIndicator",
    "SarWholeBody",
    "Sed",
    "SequenceFileOwner",
    "Stim_mon_mode",
    "Operation_mode_flag",
    "dBdt_max",
    "t_puls_max",
    "dBdt_thresh",
    "dBdt_limit",
    "SW_korr_faktor",
    "Stim_max_online",
    "Stim_max_ges_norm_online",
    "Stim_lim",
    "Stim_faktor",
    "CoilForGradient",
    "CoilTuningReflection",
    "CoilId",
    "MiscSequenceParam",
    "MrProtocolVersion",
    "MrProtocol",
    "DataFileName",
    "RepresentativeImage",
    "PositivePCSDirections",
    "RelTablePosition",
    "ReadoutOS",
    "LongModelName",
    "SliceArrayConcatenations",
    "SliceResolution",
    "MrEvaProtocol",
    "AbsTablePosition",
    "AutoAlignMatrix",
    "MeasurementIndex",
    "CoilString",
    "PATModeText",
    "PatReinPattern"
    "EchoLinePosition",
    "EchoColumnPosition",
    "EchoPartitionPosition",
    "UsedChannelMask",
    "Actual3DImaPartNumber",
    "ICE_Dims",
    "B_value",
    "Filter1",
    "Filter2",
    "ProtocolSliceNumber",
    "RealDwellTime",
    "PixelFile",
    "PixelFileName",
    "SliceMeasurementDuration",
    "SequenceMask",
    "AcquisitionMatrixText",
    "MeasuredFourierLines",
    "FlowEncodingDirection",
    "FlowVenc",
    "PhaseEncodingDirectionPositive",
    "NumberOfImagesInMosaic",
    "DiffusionGradientDirection",
    "ImageGroup",
    "SliceNormalVector",
    "DiffusionDirectionality",
    "TimeAfterStart",
    "FlipAngle",
    "SequenceName",
    "RepetitionTime",
    "EchoTime",
    "NumberOfAverages",
    "VoxelThickness",
    "VoxelPhaseFOV",
    "VoxelReadoutFOV",
    "VoxelPositionSag",
    "VoxelPositionCor",
    "VoxelPositionTra",
    "VoxelNormalSag",
    "VoxelNormalCor",
    "VoxelNormalTra",
    "VoxelInPlaneRot",
    "ImagePositionPatient",
    "ImageOrientationPatient",
    "PixelSpacing",
    "SliceLocation",
    "SliceThickness",
    "SpectrumTextRegionLabel",
    "Comp_Algorithm",
    "Comp_Blended",
    "Comp_ManualAdjusted",
    "Comp_AutoParam",
    "Comp_AdjustedParam",
    "Comp_JobID",
    "FMRIStimulInfo",
    "FlowEncodingDirectionString",
    "RepetitionTimeEffective"
    "ImageNumber",
    "ImageComments",
    "ReferencedImageSequence",
    "PatientOrientation",
    "ScanningSequence",
    "SequenceName",
    "RepetitionTime",
    "EchoTime",
    "InversionTime",
    "NumberOfAverages",
    "ImagingFrequency",
    "ImagedNucleus",
    "EchoNumbers",
    "MagneticFieldStrength",
    "NumberOfPhaseEncodingSteps",
    "EchoTrainLength",
    "PercentSampling",
    "PercentPhaseFieldOfView",
    "TriggerTime",
    "ReceivingCoil",
    "TransmittingCoil",
    "AcqusitionMatrix",
    "PhaseEncodingDirection",
    "FlipAngle",
    "VariableFlipAngleFlag",
    "SAR",
    "dBdt",
    "Rows",
    "Columns",
    "SliceThickness",
    "ImagePositionPatient",
    "ImageOrientationPatient",
    "SliceLocation",
    "EchoLinePosition",
    "EchoColumnPosition",
    "EchoPartitionPosition",
    "Actual3DImaPartNumber",
    "RealDwellTime",
    "ProtocolSliceNumber",
    "DataFile",
    "DataFileName",
    "ICE_Dims",
    "PixelSpacing",
    "SourceImageSequence",
    "PixelBandwidth",
    "SliceMeasurementDuration",
    "SequenceMask",
    "AcquisitionMatrixText",
    "MeasuredFourierLines",
    "CsiGridshiftVector",
    "RepetitionTimeEffective",
    "MoCoQMeasure",
    "BandwidthPerPixelPhaseEncode",
    "RBMoCoTrans",
    "AutoInlineImageFilterEnabled",
    "RFSWDDataType",
    "MosaicRefAcqTimes",
    "ImaPATModeText",
    "ImaCoilString",
    "SlicePosition_PCS",
    "LQAlgorithm",
    "GSWDDataType",
    "FMRIStimulLevel",
    "CsiPixelSpacing",
    "QCData",
    "MultistepIndex",
    "CsiImagePositionPatient",
    "ImaRelTablePosition",
    "OriginalImageNumber",
    "NormalizeManipulated",
    "CsiSliceThickness",
    "NonPlanarImage",
    "B_matrix",
    "ImaAbsTablePosition",
    "RBMoCoRot",
    "CsiSliceLocation",
    "CsiImageOrientationPatient",
    "OriginalSeriesNumber",
    "VFModelInfo",
    "AutoAlignData",
    "TalesReferencePower",
    "ProtocolChangeHistory",
    "PostProcProtocol",
    "FmriModelParameters",
    "SARMostCriticalAspect",
    "B1rms",
    "FmriExternalParameters",
    "PatReinPattern",
    "B1rmsSupervision",
    "FmriExternalInfo",
    "RFSWDMostCriticalAspect",
    "GradientMode",
    "FlowCompensation",
    "Isocentered",
    "FmriModelInfo",
    "RFSWDOperationMode",
    "VFSettings",
    "CoilForGradient2",
    "MrPhoenixProtocol",
    "TablePositionOrigin",
    "Laterality4MF",
    "PhaseSliceOversampling",
    "DICOMAcquisitionContrast",
    "SafetyStandard",
    "GradientEchoTrainLength",
    "DICOMImageFlavor",
    "VersionInfo",
    "RFEchoTrainLength",
    "MRVelocityEncoding",
    "UsedChannelString",
    "ExamLandmarks",
    "MRDiffusion",
    "VolumetricProperties4MF",
    "RealWorldValueMapping",
    "ExamDataRole",
    "PhaseContrastN4",
    "VelocityEncodingDirectionN4",
    "ImageType4MF",
    "ArterialSpinLabelingContrast",
    "Distorcor_IntensityCorrection",
    "MorphoQCThreshold",
    "MR_ASL",
    "ImageHistory",
    "MorphoQCIndex",
    "FmriAcquisitionDescriptionSequence",
    "FmriConditionsDataSequence",
    "FmriResultSequence",
    "RSatOrientationSag",
    # Spectroscopy
    "MixingTime",
    "DataPointRows",
    "RSatPositionSag",
    "AcquisitionMatrix",
    "NumberOfFrames",
    "RSatPositionCor",
    "VoiThickness",
    "TransmitterReferenceAmplitude",
    "ImageNumber",
    "SpectroscopyAcquisitionOut-of-planePhaseSteps",
    "WaterReferencedImageUid",
    "DataPointColumns",
    "ResonantNucleus",
    "FrequencyCorrection",
    "RSatOrientationTra",
    "DataSetInfo",
    "VoiPosition",
    "WaterReferencedPhaseCorrection",
    "VoiInPlaneRotation",
    "VoiPhaseFoV",
    "HammingFilterWidth",
    "RSatPositionTra",
    "SpectroscopyAcquisitionDataColumns",
    "SpectroscopyAcquisitionPhaseColumns",
    "VoiOrientation",
    "SpacingBetweenSlices",
    "DataRepresentation",
    "VoiReadoutFoV",
    "SignalDomainColumns",
    "RSatThickness",
    "RSatOrientationCor",
    "SpectroscopyAcquisitionPhaseRows",
    "k-spaceFiltering",
    # VE11A
    "ConfigFileInfo",
    "AASpineModelVerificationStatus",
    "AASpineModelData",
    "UserDefinedSeries",
    "UserDefinedImage",
    "UserDefinedRaw",
    # VE11C
    "ConditionalImplantScanMode"
]

_syngodtype_for_vr = {
    "UN":  0,
    "DS":  3,
    "FD":  4,
    "FL":  5,
    "IS":  6,
    "SL":  7,
    "SS":  8,
    "UL":  9,
    "US": 10,
    "CS": 16,
    "LO": 19,
    "LT": 20,
    "SH": 22,
    "ST": 23,
    "UI": 25,
    "UT": 27
}


# TODO check if we need to map bytes to str here.
def read_header(f):
    """
    Read Siemens CSA header from a file like object.

    Returns the number of tags expected.
    """
    # NB: byte order is *always* little endian
    s = Struct('<4s4sII')
    s1, s2, ntags, i = s.unpack(f.read(s.size))
    if s1 != b'SV10' or s2 != b'\4\3\2\1':
        raise ValueError('Not a valid SV10 CSA2 header')
    if i != 77:
        raise ValueError('Missing "M" at offset 12')
    return ntags


def read_tag(f):
    """
    Read a single CSA tag from a file like object.

    Returns a tuple (tagname, vr, value) if vm == 1
    else (tagname, vr, [list of values]) if vm>1
    """
    s = Struct('<64sI2sxxIII')
    name, vm, vr, syngodtype, nitems, xx = s.unpack(f.read(s.size))

    # Need to clean up the string as we'll get the nulls as well
    name = name.split(b'\0')[0].decode('ascii', errors='ignore')
    vr = vr.split(b' ')[0].decode('ascii', errors='ignore')

    if _syngodtype_for_vr[vr] != syngodtype:
        warn('Inconsistent types %d/%s' % (syngodtype, vr))
    if xx not in (77, 205):
        warn('Unexpected value in tag header xx=%d' % xx)

    # Empty tag
    if not nitems:
        return (name, vr, '')

    # Generally exactly 6 items of which only the first vm are non-empty
    tag_items = []
    for i in range(nitems):
        s = Struct('<IIII')
        i0, fieldlen, i2, i3 = s.unpack(f.read(s.size))
        if i2 not in (77, 205):
            warn('Unexpected value in item header i2=%d' % i2)
        if fieldlen > 0:
            s = Struct('<%ds' % fieldlen)
            field, = s.unpack(f.read(s.size))
            field = field.decode('ascii', errors='ignore')

            # pad out to a 4 byte alignment
            f.read((4 - fieldlen % 4) % 4)
            tag_items.append(field.split('\0')[0].strip() if field else '')
        else:
            # ignore missing entries
            pass
            # tag_items.append('')

    if vm < 1:
        # sometimes vm is zero - return all the elements as a list
        return name, vr, tag_items
    elif vm == 1:
        return name, vr, tag_items[0]
    elif vm < len(tag_items):
        return name, vr, tag_items[:vm]
    else:
        return name, vr, tag_items


def map_vrs(tags):
    """
    Map 'dicom like' VR codes to numeric or plain string values.

    Tags is a list of tags in the form (name, vr, stringvalue)
    """
    vrtypes = {
        "UN": str,
        "DS": float,
        "FD": float,
        "FL": float,
        "IS": int,
        "SL": int,
        "SS": int,
        "UL": int,
        "US": int,
        "CS": str,
        "LO": str,
        "LT": str,
        "SH": str,
        "ST": str,
        "UI": str,
        "UT": str
    }

    typed_tags = []
    for (name, vr, value) in tags:
        try:
            if isinstance(value, str):
                typed_tags.append(
                    (name, vrtypes[vr](value) if value else '')
                )
            else:
                typed_tags.append(
                    (name, [vrtypes[vr](v) if v else '' for v in value])
                )
        except ValueError:
            typed_tags.append((name, value))

    return typed_tags


def csa(dobj, section='Series', show_phoenix=True):
    """
    Dictionary of CSA tags of the given section from a pydicom dataset object.

    Parameters
    ----------
    dobj : pydicom dataset
        Dataset containing Siemens Series or Image CSA shadow headers.
    section : string (optional)
       'Series' or 'Image'
    show_phoenix : bool
       Show the raw dump of the phoenix protocol (otherwise hidden)

    Results
    -------
    A dictionary of CSA tags.
    Values are converted to python float, int or str based on syngo datatype.

    """
    priv_creators = [
        # work around for non dictionary-like behaviour of dicom obj
        key for key in dobj.keys()
        if dobj[key].name == 'Private Creator' and dobj[key].value == 'SIEMENS CSA HEADER'
    ]
    if not priv_creators:
        raise AttributeError('Dicom object does not have a Siemens CSA Header')
    priv_creator = priv_creators[0]

    group, element_base = priv_creator.group, 256 * priv_creator.element

    CSAImageHeaderType     = (group, element_base + 0x08)
    CSAImageHeaderVersion  = (group, element_base + 0x09)
    CSAImageHeaderInfo     = (group, element_base + 0x10)
    CSASeriesHeaderType    = (group, element_base + 0x18)
    CSASeriesHeaderVersion = (group, element_base + 0x19)
    CSASeriesHeaderInfo    = (group, element_base + 0x20)

    if section.lower() == 'image':
        dicomtag = CSAImageHeaderInfo
    elif section.lower() == 'series':
        dicomtag = CSASeriesHeaderInfo
    else:
        raise ValueError('Unrecognised Section %s' % section)

    try:
        tagvalue = dobj[dicomtag].value
    except KeyError:
        raise AttributeError('Missing Siemens CSA %s section' % section)
    f = BytesIO(tagvalue)
    ntags = read_header(f)
    tags = [read_tag(f) for i in range(ntags)]
    csa_tag_dict = dict(map_vrs(tags))
    f.close()

    for key in csa_tag_dict:
        if key not in _known_csa_tags:
            warn('Unexpected tag name %s in %s section' % (key, section))

    if dicomtag == CSASeriesHeaderInfo and not show_phoenix:
        if 'MrPhoenixProtocol' in csa_tag_dict:
            csa_tag_dict['MrPhoenixProtocol'] = '<Phoenix Protocol>'
    return csa_tag_dict


# phoenix moved to separate module - stop gap to alias it here
# careful about circular import
# from . siemensphoenix import phoenix


def main():
    from argparse import ArgumentParser, FileType
    from pprint import pprint
    from pydicom import dcmread

    parser = ArgumentParser(
        description='Display Siemens CSA headeers',
        add_help=True
    )

    parser.add_argument(
        'infile',
        action='store', type=FileType('rb'),
        help='(Siemens MR) DICOM file to read'
    )

    args = parser.parse_args()

    dobj = dcmread(args.infile)

    ser_csa = csa(dobj, 'Series', show_phoenix=False)
    print('Series CSA Header:')
    pprint(ser_csa)

    img_csa = csa(dobj, 'Image')
    print('Image CSA Header:')
    pprint(img_csa)

if __name__ == '__main__':
    main()
