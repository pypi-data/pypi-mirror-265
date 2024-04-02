# Extra DICOM support including Siemens Images

This package provides some additional routines for use with
[pydicom](http://www.pydicom.org/) for access to the hidden fields in Siemens
images and for handling stacks and series of images.

The main Siemens related functions are the modules:
 - siemenscsa: access to Siemens CSA shadow tags and phoenix protocol info
 - siemensoog: access to Siemens CSA MEDCON graphics overlays

There is also an experimental dicom to json converter (`dcm2js`) that extracts
sequence parameters that are useful for the fMRI/DTI processing pipelines.

The extraction of the graphics overlay is partial and ad hoc and was intended
for use in extracting the regions of interest that had been drawn on CMR images
within the Siemens Argos analsysis tools. We don't have sufficient information
about the modified STP/STEP format used to extract the graphics reliably for all
images.
