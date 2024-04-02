#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Tools for extracting information from Siemens DICOM Phoenix protocols.
"""
import re
from functools import partial

from dcmextras.siemenscsa import csa

__all__ = ['phoenix']


def get_private_tag(dobj, section, offset):
    """
    Get private tag at given offset.
    """
    priv_creators = [
        # work around for non dictionary-like behaviour of dicom obj
        key for key in dobj.keys()
        if dobj[key].name == 'Private Creator' and dobj[key].value == section
    ]

    if priv_creators:
        priv_creator = priv_creators[0]
        group, element_base = priv_creator.group, 256 * priv_creator.element
        return dobj[group, element_base + offset]
    return None


def get_sds_tag(dobj, offset):
    """
    Get Siemens XA11 series level private data tag at given offset.
    """
    item = get_private_tag(dobj, 'SIEMENS MR SDS 01', offset)
    if item is not None:
        return item.value
    if 'SharedFunctionalGroupsSequence' in dobj:
        sfgs = dobj.SharedFunctionalGroupsSequence[0]
        privseq = get_private_tag(sfgs, 'SIEMENS MR SDS 01', 0xfe)
        item = get_private_tag(privseq[0], 'SIEMENS MR SDS 01', offset)
        if item is not None:
            return item.value
        return None


class defaultlist(list):
    """
    List that supports default values up to a prespecified size.

    Grows if indexed over current size and default allocates new values
    It needs to do this rather than just return them as items may be mutable
    """

    def __init__(self, size):
        self._size = size
        self._type = None

    def __getitem__(self, key):
        if isinstance(key, slice):
            return [self.__getitem__(i) for i in range(*key.indices(self._size))]
        elif isinstance(key, int):
            if key < 0:
                key += self._size
            try:
                return super(defaultlist, self).__getitem__(key)
            except IndexError:
                if key >= self._size:
                    # unexpected - grow list to encompass
                    self._size = key + 1
                if self._type is not None:
                    self += [
                        self._type()
                        for i in range(1+key-len(self))
                    ]
                    return super(defaultlist, self).__getitem__(key)
                else:
                    return None
        else:
            return super(defaultlist, self).__getitem__(key)

    def __setitem__(self, key, value):
        # first assignment sets type
        if isinstance(key, slice):
            for i, v in zip(range(*key.indices(self._size)), value):
                self.__setitem__(i, v)
        elif isinstance(key, int):
            if key < 0:
                key += self._size
            if self._type is None:
                self._type = type(value)
            try:
                super(defaultlist, self).__setitem__(key, value)
            except IndexError:
                if key >= self._size:
                    # unexpected - grow list to encompass
                    self._size = key + 1
                self += [self._type() for i in range(1+key-len(self))]
                super(defaultlist, self).__setitem__(key, value)
        else:
            super(defaultlist, self).__setitem__(key, value)

    def __delitem__(self, key):
        if isinstance(key, slice):
            for i in reversed(range(*key.indices(self._size))):
                self.__delitem__(i)
        elif isinstance(key, int):
            if key < 0:
                key += self._size
            if key < len(self):
                super(defaultlist, self).__delitem__(key)
            if key >= self._size:
                # pass up to raise IndexError
                super(defaultlist, self).__delitem__(key)
        else:
            super(defaultlist, self).__delitem__(key)

    def fill(self):
        self.__getitem__(self._size-1)


class objdict(dict):
    """Dictionary that supports attribute style access to keys."""

    def __getattr__(self, name):
        if name in self:
            return self[name]
        else:
            raise AttributeError("No such attribute: " + name)


def split_tag_path(tag):
    """Split attribute style (with dots) name into a list of components."""
    assert isinstance(tag, str) and '..' not in tag
    return tag.strip().split('.')


def split_tag_hungarian(tag):
    """Split off hungarian notation prefix from attribute name."""
    assert isinstance(tag, str)
    name = tag.strip()
    regex = r'([a-z]{1,3})([A-Z].*)'
    match = re.match(regex, name)
    return match.groups() if match else ('', name)


def split_tag_array(tag):
    """Split name including an index into a separate name and index."""
    assert isinstance(tag, str) and '[' in tag and ']' in tag
    return tag.split('[')[0], int(tag.split('[')[1].split(']')[0])


def ensure_dict_at(context, name):
    """Add a dictionary node (if need be) and return it as the new context."""
    if name not in context:
        context[name] = objdict()
    return context[name]


def ensure_dict_in_list_at(context, name, index):
    """
    Make sure item at index in (previously allocated) list at node is objdict.

    Return the dictionary at the given index as the new context
    """
    # assume list is already allocated
    assert name in context and isinstance(context[name], defaultlist)
    context = context[name]
    if not isinstance(context[index], objdict):
        # this will force type to objdict and expand size to index+1
        context[index] = objdict()
    return context[index]


def guess_type(value):
    """Try and coerce the type of a value based on guesswork."""
    if isinstance(value, str):
        for fn in [int, partial(int, base=16), float, str]:
            try:
                return fn(value)
            except ValueError:
                pass
    return value


def special_case_type(name, value):
    """Determine a python type based on known names of elements."""
    if '[' in name:
        name, index = split_tag_array(name)
    if name in [
        'IdPart'
    ]:
        return int
    elif name in [
        'MaxOnlineTxAmpl',
        'WorstCaseMaxOnlineTxAmpl',
    ]:
        return float
    else:
        return None


def type_map(name, prefix, value):
    """Try and coerce the type of a value based on a hungarian prefix etc."""
    if '[' in name:
        name, index = split_tag_array(name)
    vtype = special_case_type(name, value)
    if vtype is not None:
        return vtype(value)

    def int_(x):
        """Integer possibly encoded as a numeric string, maybe as hex."""
        return int(x, 16) if isinstance(x, str) and 'x' in x else int(x)

    if prefix:
        type_dict = {
            'fl': float,
            'afl': float,
            'd': float,
            'ad': float,
            'l': int_,
            'al': int_,
            'uc': int_,
            'ul': int_,
            'b': lambda s: bool(int_(s)),
            't': str,

        }
        for k in type_dict.keys():
            if prefix.startswith(k):
                return type_dict[k](value)
    return guess_type(value)


class Complexifier:
    """
    Replaces dicts representing complex numbers with standard python complex.

    Recursive 'visitor' to traverse data structure.
    """

    def visit(self, node):
        method = getattr(self, 'visit_' + type(node).__name__, None)
        return method(node) if method is not None else node

    def visit_objdict(self, node):
        if {'Im', 'Re'}.intersection(set(node)):
            # terminal complex scalar
            return complex(getattr(node, 'Re', 0.0), getattr(node, 'Im', 0.0))
        else:
            return objdict({k: self.visit(v) for k, v in node.items()})

    def visit_defaultlist(self, node):
        list_ = defaultlist(node._size)
        compound = all(isinstance(item, objdict) for item in node)
        complex_like = compound and {'Im', 'Re'}.intersection(
            set().union(*(set(item) for item in node))
        )
        if complex_like:
            # terminal complex list
            list_[:] = [
                complex(getattr(item, 'Re', 0.0), getattr(item, 'Im', 0.0))
                for item in node
            ]
        else:
            list_[:] = [self.visit(item) for item in node]
        return list_


def parse_tags(rawdict):
    """
    Convert flat protocol dictionary to heirarchical structure.

    The raw form of the protocol dictionary is flat with the structured strings
    as keys. This constructs a hierarchical data structure based on the
    structure of the keys in the raw form.

    It uses modified dictionary and list types to provide a attribute like
    access and to allow for incompletely defined lists with default values.

    It is traversable with attribute access and list index notation that
    mirrors the pths in the original keys..
    """
    root = objdict()
    for tagname, value in rawdict.items():
        path = split_tag_path(tagname)
        nelements = len(path)
        context = root
        for i, element in enumerate(path):
            # remove any hungarian prefix
            prefix, name = split_tag_hungarian(element)
            # allocator element for array, these names duplicate the tag name
            # of the list without the brackets - just ignore the maximum size
            # and create an empty list at this point under the tagname
            # nb: it seems they are not always present so list creation will
            # also have to be handled below
            if i == nelements - 3 and path[-2:] == ['__attribute__', 'size']:
                if name not in context:
                    context[name] = defaultlist(int(value))
                break

            terminal = i == nelements - 1
            if terminal:
                if '[' in name:
                    # a terminal list - insert element in list under base name
                    name, index = split_tag_array(name)
                    if name not in context:
                        # list not previously allocated
                        context[name] = defaultlist(index+1)
                    context[name][index] = type_map(name, prefix, value)
                else:
                    # a terminal scalar - insert in dict under name
                    context[name] = type_map(name, prefix, value)
            else:
                if '[' in name:
                    # non terminal array is always an array of structs
                    name, index = split_tag_array(name)
                    if name not in context:
                        # list not previously allocated
                        context[name] = defaultlist(index+1)
                    context = ensure_dict_in_list_at(context, name, index)
                else:
                    # non terminal scaler is always a single struct
                    context = ensure_dict_at(context, name)
    return root


def phoenix(dobj, raw=True):
    """
    Get Phoenix protocol as a python dictionary.

    Takes a pydicom dataset.

    The values are all strings and the keys are uninterpreted
    so we have keys like 'sGRADSPEC.sEddyCompensationZ.aflTimeConstant[0]'
    and so on. This is based on parsing the 'ASCCONV' section.

    Parameters
    ----------
    dobj : pydicom dataset
        Dataset containing Siemens Series CSA shadow header.
    raw : bool
        Whether to leave as flat or reformat as recursive datastructure
    Results
    -------
    A recursive dictionary of Phoenix protocol tags, traversable by
    attribute access or a flat dictionary with uninterpreted keys

    """
    # The Phoenix Protocol is in the Series section
    try:
        phoenixtag = csa(dobj, 'Series', show_phoenix=True)['MrPhoenixProtocol']
    except AttributeError:
        # XA10, XA11
        phoenixtag = get_sds_tag(dobj, 0x19).decode('utf-8')
    if phoenixtag is None:
        raise AttributeError('Phoenix structure not available in DICOM object')

    # Split off the ASCCONV section which is delimited by
    # the string  '### ASCCONV BEGIN ###' .. '### ASCCONV END ###'
    p = re.compile(r'### ASCCONV (?:BEGIN|END) [^#]*###')
    sections = p.split(phoenixtag)
    if len(sections) != 3:
        raise ValueError('Cannot extract ASCCONV section %d' % len(sections))
    ascconv = sections[1]

    # Unfortunately, we still have doubled up quotes
    # so we'll strip them down to single quotes here
    ascconv = re.sub(r'""""', r'""', ascconv)
    ascconv = re.sub(r'"("[^"]+")"', r'\1', ascconv)

    # Build dict - must preserve insertion order (python3.6+ OK) so array "allocators" come before array items
    protocol = dict()

    for line in ascconv.split('\n'):
        # 'ini' style key value pairs
        tagval = line.split('=')
        if len(tagval) == 2:
            # strip redundant space and remove embedded quotes
            tag, value = tagval[0].strip(), tagval[1].strip()
            if '#' in value:
                value = value.split('#')[0].rstrip()
            if value == r'""':
                value = ''
            else:
                value = re.sub(r'"("[^"]+")"', r'\1', value)
            if value.startswith('"'):
                value = value.strip('"')
            else:
                value = guess_type(value)
            protocol[tag] = value

    if not raw:
        protocol = Complexifier().visit(parse_tags(protocol))
    return protocol


def main():
    from argparse import ArgumentParser, FileType
    from pprint import pprint
    from pydicom import dcmread

    parser = ArgumentParser(
        description='Display Siemens Phoenix Protocol',
        add_help=True
    )

    parser.add_argument(
        '--raw', '-r',
        action='store_true', default=False,
        help='print flat dictionary without interpretation',
    )
    parser.add_argument(
        'infile',
        action='store', type=FileType('rb'),
        help='(Siemens MR) DICOM file to read'
    )

    args = parser.parse_args()

    dobj = dcmread(args.infile)
    protocol = phoenix(dobj, raw=args.raw)
    pprint(objdict(protocol))


if __name__ == "__main__":
    main()
