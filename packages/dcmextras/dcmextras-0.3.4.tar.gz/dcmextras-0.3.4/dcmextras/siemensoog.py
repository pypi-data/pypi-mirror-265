#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''Tools for extracting graphics inaformation from Siemens DICOM. These are in a
   cad/cam format (step) that we have only partially reverse engineered here
   for inter-operability.
'''
import sys


class CsaError(Exception):
    pass


class CsaObject(object):
    def __init__(self, objid, plist):
        self.objid = objid
        self.parentid = None
        self.childids = []
        self.parent = None
        self.children = []

    def print_obj(self, printfn=None, level=0):
        if printfn is None:
            print('--'*level, type(self))
        for obj in self.children:
            obj.print_obj(printfn, level+1)

    def assemble(self, objdict):
        if self.parentid in objdict:
            self.parent = objdict[self.parentid]
        self.children = [objdict[childid] for childid in self.childids if childid in objdict]
        for child in self.children:
            child.assemble(objdict)


class CsaImageOverlay(CsaObject):
    # normally top level container with CsaGraphicPrimGroup as a child
    def __init__(self, objid, plist):
        super(CsaImageOverlay, self).__init__(objid, plist)
        self.childids = plist[13]
        self.overlayname = plist[32]


class CsaGraphicPrimGroup(CsaObject):
    # may have other prim groups, polygons, text or boxes as children
    def __init__(self, objid, plist):
        super(CsaGraphicPrimGroup, self).__init__(objid, plist)
        self.pointvectorid = plist[6]
        if plist[11] is not None:
            # when parent is another CsaGraphicPrimGroup
            self.parentid = plist[11]
        elif plist[12] is not None:
            # when parent is a CsaImageOverlay
            self.parentid = plist[12]

        self.childids = plist[16]


class CsaGraphicAxis(CsaObject):
    # may have other prim groups, polygons, text or boxes as children
    def __init__(self, objid, plist):
        super(CsaGraphicAxis, self).__init__(objid, plist)
        self.pointvectorid = plist[6]
        self.parentid = plist[11]
        self.childids = plist[16]
        self.points = []

    def print_obj(self, printfn=None, level=0):
        if printfn is None:
            print('--'*level, 'Axis @', self.points, ':')
        for obj in self.children:
            obj.print_obj(printfn, level+1)

    def assemble(self, objdict):
        if self.pointvectorid in objdict:
            self.points = objdict[self.pointvectorid].points
        super(CsaGraphicAxis, self).assemble(objdict)


class CsaGraDoubleVec3DArray(CsaObject):
    # always leaf objects
    def __init__(self, objid, plist):
        super(CsaGraDoubleVec3DArray, self).__init__(objid, plist)
        coordlist = plist[1]
        self.points = list(zip(coordlist[0::3], coordlist[1::3], coordlist[2::3]))


class CsaGraphicPixmap(CsaObject):
    # always leaf objects
    # CsaGraphicPixmap(0, '1\#f00\0\#000\0110\1111\1111\0110', 8, 1, 1, 4, 4, 2, 1, '414420091013132047.234000CSAPIXMAP')
    def __init__(self, objid, plist):
        super(CsaGraphicPixmap, self).__init__(objid, plist)
        self.pixmapstring = plist[1]
        self.pixmap = None


class CsaGraphicPolygon(CsaObject):
    # generally parented by a prim group and have a CsaGraDoubleVec3DArray child
    def __init__(self, objid, plist):
        super(CsaGraphicPolygon, self).__init__(objid, plist)
        # -> n point list
        self.pointvectorid = plist[6]
        self.parentid = plist[11]
        self.points = []
        # seem to have a CsaGraVVIDictionary at 13 and a CsaUVString at 14 or '$'

    def print_obj(self, printfn=None, level=0):
        if printfn is None:
            print('--'*level, 'Polygon:')
            print('--'*(level+1), self.points)
        else:
            printfn('Polygon', self.points)

    def assemble(self, objdict):
        if self.pointvectorid in objdict:
            self.points = objdict[self.pointvectorid].points
        super(CsaGraphicPolygon, self).assemble(objdict)


class CsaGraphicPolyLine(CsaObject):
    # generally parented by a prim group and have a CsaGraDoubleVec3DArray child
    def __init__(self, objid, plist):
        super(CsaGraphicPolyLine, self).__init__(objid, plist)
        # -> n point list
        self.pointvectorid = plist[6]
        self.parentid = plist[11]
        self.points = []

    def print_obj(self, printfn=None, level=0):
        if printfn is None:
            print('--'*level, 'PolyLine:')
            print('--'*(level+1), self.points)
        else:
            printfn('PolyLine', self.points)

    def assemble(self, objdict):
        if self.pointvectorid in objdict:
            self.points = objdict[self.pointvectorid].points
        super(CsaGraphicPolyLine, self).assemble(objdict)


class CsaGraphicArrow(CsaObject):
    # generally parented by a prim group and have a CsaGraDoubleVec3DArray child
    def __init__(self, objid, plist):
        super(CsaGraphicArrow, self).__init__(objid, plist)
        # -> n point list
        self.pointvectorid = plist[6]
        self.parentid = plist[11]
        self.points = []

    def print_obj(self, printfn=None, level=0):
        if printfn is None:
            print('--'*level, 'Arrow:')
            print('--'*(level+1), self.points)
        else:
            printfn('Arrow', self.points)

    def assemble(self, objdict):
        if self.pointvectorid in objdict:
            self.points = objdict[self.pointvectorid].points
        super(CsaGraphicArrow, self).assemble(objdict)


class CsaGraphicText(CsaObject):
    # generally parented by a prim group
    def __init__(self, objid, plist):
        super(CsaGraphicText, self).__init__(objid, plist)
        # could be the location - it's a single point
        self.pointvectorid = plist[6]
        self.parentid = plist[11]
        # seem to have a CsaGraVVIDictionary at 13 and a CsaUVString at 14 or just '$'
        charlist = plist[43]
        legendtext = ''.join([chr(i) for i in charlist[0:-1]])
        self.legendlines = legendtext.split('\r\n')
        self.points = []

    def print_obj(self, printfn=None, level=0):
        if printfn is None:
            print('--'*level, 'Text @', self.points, ':')
            for line in self.legendlines:
                print('--'*(level+1), line)
        else:
            printfn('Text', self.points[0], self.legendlines)

    def assemble(self, objdict):
        if self.pointvectorid in objdict:
            self.points = objdict[self.pointvectorid].points
        super(CsaGraphicText, self).assemble(objdict)


class CsaGraphicSquare(CsaObject):
    # generally parented by a prim group and have a CsaGraDoubleVec3DArray child
    def __init__(self, objid, plist):
        super(CsaGraphicSquare, self).__init__(objid, plist)
        # -> 4 point list
        self.pointvectorid = plist[6]
        self.parentid = plist[11]
        self.points = []

    def print_obj(self, printfn=None, level=0):
        if printfn is None:
            print('--'*level, 'Square:')
            print('--'*(level+1), self.points)
        else:
            printfn('Square', self.points)

    def assemble(self, objdict):
        if self.pointvectorid in objdict:
            self.points = objdict[self.pointvectorid].points
        super(CsaGraphicSquare, self).assemble(objdict)


class CsaGraphicCircle(CsaObject):
    # generally parented by a prim group and have a CsaGraDoubleVec3DArray child
    def __init__(self, objid, plist):
        super(CsaGraphicCircle, self).__init__(objid, plist)
        # -> 4 point list
        self.pointvectorid = plist[6]
        self.parentid = plist[11]
        self.points = []

    def print_obj(self, printfn=None, level=0):
        if printfn is None:
            print('--'*level, 'Circle:')
            print('--'*(level+1), self.points)
        else:
            printfn('Circle', self.points)

    def assemble(self, objdict):
        if self.pointvectorid in objdict:
            self.points = objdict[self.pointvectorid].points
        super(CsaGraphicCircle, self).assemble(objdict)


class CsaGraphicLine(CsaObject):
    # generally parented by a prim group and have a CsaGraDoubleVec3DArray child
    def __init__(self, objid, plist):
        super(CsaGraphicLine, self).__init__(objid, plist)
        # -> 2 point list
        self.pointvectorid = plist[6]
        self.parentid = plist[11]
        self.points = []

    def print_obj(self, printfn=None, level=0):
        if printfn is None:
            print('--'*level, 'Line:')
            print('--'*(level+1), self.points)
        else:
            printfn('Line', self.points)

    def assemble(self, objdict):
        if self.pointvectorid in objdict:
            self.points = objdict[self.pointvectorid].points
        super(CsaGraphicLine, self).assemble(objdict)


class CsaGraphicMarker(CsaObject):
    # generally parented by a prim group and have a CsaGraDoubleVec3DArray child
    def __init__(self, objid, plist):
        super(CsaGraphicMarker, self).__init__(objid, plist)
        # -> 2 point list
        self.pointvectorid = plist[6]
        self.parentid = plist[11]
        self.pixmapid = plist[47]
        self.pixmap = None
        self.points = []

    def print_obj(self, printfn=None, level=0):
        if printfn is None:
            print('--'*level, 'Marker:')
            print('--'*(level+1), self.points, self.pixmap)
        else:
            printfn('Marker', self.points, self.pixmap)

    def assemble(self, objdict):
        if self.pointvectorid in objdict:
            self.points = objdict[self.pointvectorid].points
        if self.pixmapid in objdict:
            self.pixmap = objdict[self.pixmapid].pixmap
        super(CsaGraphicMarker, self).assemble(objdict)


class CsaUVString(CsaObject):
    #  a leaf object generally referenced from a CsaGraphicText or CsaGraVVIDictionary
    def __init__(self, objid, plist):
        super(CsaUVString, self).__init__(objid, plist)
        charlist = plist[1]
        self.text = ''.join([chr(i) for i in charlist[0:-1]])


class CsaGraphicFrameApplContainer(CsaObject):
    #  a leaf object (?) generally referenced from a CsaGraphicText
    def __init__(self, objid, plist):
        super(CsaGraphicFrameApplContainer, self).__init__(objid, plist)
        charlist = plist[1]
        self.text = ''.join([chr(i) for i in charlist[0:-1]])


class CsaGraVVIDictionary(CsaObject):
    # contains two reference lists, the first to CsaUVString and the second to CsaGraphicFrameApplContainer
    # both of which seem to be leaves, it also has a long list of -1 and 0
    def __init__(self, objid, plist):
        super(CsaGraVVIDictionary, self).__init__(objid, plist)
        self.childids = plist[1] + plist[2]


class SiemensOOG(object):
    def __init__(self, dobj):
        self.objdict = self._get_objdict(dobj)
        self._assemble_tree()

    def _get_objdict(self, dobj):
        '''Return a dictionary of structures on a slice. The dictionary keys are the names of the structure
        and there are fields for the contour pts, the etx associated with the structure and the box (of unknown
        meaning so far)
        '''
        typedict = {
            'CsaImageOverlay': CsaImageOverlay,
            'CsaGraphicPrimGroup': CsaGraphicPrimGroup,
            'CsaGraphicAxis': CsaGraphicAxis,
            'CsaGraDoubleVec3DArray': CsaGraDoubleVec3DArray,
            'CsaGraphicPixmap': CsaGraphicPixmap,
            'CsaGraphicPolygon': CsaGraphicPolygon,
            'CsaGraphicPolyLine': CsaGraphicPolyLine,
            'CsaGraphicArrow': CsaGraphicArrow,
            'CsaGraphicText': CsaGraphicText,
            'CsaGraphicSquare': CsaGraphicSquare,
            'CsaGraphicCircle': CsaGraphicCircle,
            'CsaGraphicLine': CsaGraphicLine,
            'CsaGraphicMarker': CsaGraphicMarker,
            'CsaUVString': CsaUVString,
            'CsaGraphicFrameApplContainer': CsaGraphicFrameApplContainer,
            'CsaGraVVIDictionary': CsaGraVVIDictionary
        }

        for element in range(0x0010, 0x0100):
            if (0x0029, element) in dobj and 'OOG' in dobj[0x0029, element].value:
                oog_private_tag = (0x0029,  0x100 * element + 0x10)
                break
        else:
            raise CsaError('No Private Element Block reserved for Siemens MEDCOM OOG Graphics in Dicom Object')
        try:
            stepstring = dobj[oog_private_tag].value
        except KeyError:
            raise CsaError('No Siemens MEDCOM OOG Graphics Element Found in Dicom Object')

        steplines = stepstring.decode('ascii', errors='ignore').split('\n')
        # first parse into an accessible form
        paramlistdict = {}
        for line in steplines:
            if not line.startswith('@'):
                continue
            line = line[1:]
            lhs, rhs = line.split('=')
            lhs = int(lhs)
            rhs = rhs.strip()
            if not rhs.startswith('Csa'):
                print("Unrecognised Record", rhs, file=sys.stderr)
                continue
            openp = rhs.find('(')
            closep = rhs.rfind(')')
            objtype = rhs[0:openp]
            if objtype not in typedict:
                print("Unrecognised Object Type", objtype, file=sys.stderr)
                continue

            paramstring = rhs[openp:closep+1]
            paramstring = paramstring.replace('#', '')
            paramstring = paramstring.replace('$', 'None')
            paramstring = paramstring.replace('(', '[')
            paramstring = paramstring.replace(')', ']')
            params = eval(paramstring)
            paramlistdict[lhs] = (objtype, params)

        objdict = {}
        for k, v in list(paramlistdict.items()):
            objdict[k] = typedict[v[0]](*v)
        return objdict

    def _assemble_tree(self):
        '''Pass though objects in dictionary linking them together into (usually only one) tree structures.
        '''
        objdict = self.objdict
        for overlayid in (key for key, value in objdict.items() if isinstance(value, CsaImageOverlay)):
            objdict[overlayid].assemble(objdict)

    def extract_contours(self):
        ''' Return simple dictionary of ROI's hashed on the ROI name. Contains contours, text and a 'box'.
        '''
        objdict = self.objdict

        # then tease out the contours
        structures = {}
        for overlayid in [key for (key, value) in objdict.items() if isinstance(value, CsaImageOverlay)]:
            overlay = objdict[overlayid]
            overlayname = overlay.overlayname
            primgroup = overlay.children[0]
            assert isinstance(primgroup, CsaGraphicPrimGroup)

            points = boxpoints = legendlines = []
            for obj in primgroup.children:
                if isinstance(obj, CsaGraphicPolygon):
                    points = [(x, y) for (x, y, z) in obj.points]
                elif isinstance(obj, CsaGraphicText):
                    legendlines = obj.legendlines
                elif isinstance(obj, CsaGraphicSquare):
                    boxpoints = [(x, y) for (x, y, z) in obj.points]

            structures[overlayname] = {'contour': points, 'box': boxpoints, 'legend': legendlines}

        return structures

    def print_all(self, print_fn=None):
        objdict = self.objdict
        for obj in [value for value in objdict.values() if isinstance(value, CsaImageOverlay)]:
            obj.print_obj(print_fn)


if __name__ == '__main__':
    try:
        from pydicom import dcmread
    except ImportError:
        from dicom import read_file as dcmread

    if len(sys.argv) > 1:
        dobj = dcmread(sys.argv[1])
        oog = SiemensOOG(dobj)
        oog.print_all(print)
    else:
        print('%s: No input file specified' % sys.argv[0])
