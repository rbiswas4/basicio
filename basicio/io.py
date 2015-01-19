#!/usr/bin/env python

import numpy as np
import os.path
import cStringIO
from basicio import utils
import os

_here  = os.path.dirname(os.path.realpath(__file__))

def file2strarray(file, buffer=False, delimitter='', datastring=None):
    """
    load table-like data having consistent columns in a file or string into a
    numpy array of strings


    Parameters
    ----------
    file: string, mandatory
        absolute path to file containing the data, or a string containing the
        data (with rows separated by new line characters). If file is not the
        path to a file, then buffer must be true
    buffer: optional, bool, defaults to False
        If file is a string rather than the path to a file, this must be true
    delimitter: string, optional, defaults to ''
        type of delimitter used in the file
    datastring: string, optional, defaults to `None`
        if not none, assume that all lines containing data are prepended by
        this string; therefore select only such lines, and strip this character
        off.


    Returns
    -------
    `numpy.ndarray` of strings


    Examples
    --------
    >>> fname = os.path.join(_here,'example_data/table_data.dat')
    >>> d = file2strarray(fname)
    >>> type(d)
    <type 'numpy.ndarray'>
    >>> # One can access the elements in the usual `numpy.ndarray` way
    >>> d[1, 3]
    '4.6774e-04'
    >>> print np.shape(d)
    (96, 27)
    >>> fp = open(fname)
    >>> contents = fp.read()
    >>> fp.close()
    >>> dd = file2strarray(contents, buffer=True)
    >>> (d == dd).all()
    True
    >>> fname = os.path.join(_here,'example_data/table_data_ps.dat')
    >>> x = file2strarray(fname, datastring='SN:')
    >>> np.shape(x)
    (2, 27)


    .. note:: 1. Cofirmation of buffer was introduced in order to prevent \
            errors where an incorrect filename passed was interpreted as a \
            buffer.

    """
    # Check if this is a path to a file or a string
    if os.path.isfile(file):
        fp = open(file)
    else:
        # this is a string, Check if buffer is true
        if not buffer:
            raise ValueError('The file does not exist, and buffer is False,\
                             so cannot iterpret as data stream')
        fp = cStringIO.StringIO(file)

    line = fp.readline()
    line  = line.strip()
    data = []

    while line != '':
        if datastring is None:
            lst = utils.tokenizeline(line, delimitter=delimitter)[0]
            data.append(lst)
        elif line.startswith(datastring):
            lst = utils.tokenizeline(line, delimitter=delimitter,
                                     prependstring='SN:')[0]
            data.append(lst)

        line = fp.readline()
        line  = line.strip()
    fp.close()
    data = np.asarray(data)
    return data
    
def arraydtypes(stringarray, names=None, titles=None, types=None,
                returndtype=True):
    """
    returns a list of types of columns in a 2D array of strings
    Parameters
    ----------
    stringarray: 2D array of strings, mandatory
        input array 
    

    Returns
    -------
    list of types

    
    Examples
    --------
    >>> fname = os.path.join(_here,'example_data/table_data.dat')
    >>> d = file2strarray(fname)
    >>> types = arraydtypes(d, returndtype=False)
    >>> types[0]
    'a20'
    >>> types[1]
    'f4'
    >>> types[2]
    'f4'
    >>> types[-4]
    'i8'
    >>> arraydtypes(d)
    dtype([('f0', 'S20'), ('f1', '<f4'), ('f2', '<f4'), ('f3', '<f4'), ('f4', '<f4'), ('f5', '<f4'), ('f6', '<f4'), ('f7', '<f4'), ('f8', '<f4'), ('f9', '<f4'), ('f10', '<f4'), ('f11', '<f4'), ('f12', '<f4'), ('f13', '<f4'), ('f14', '<f4'), ('f15', '<f4'), ('f16', '<f4'), ('f17', '<i8'), ('f18', '<f4'), ('f19', '<f4'), ('f20', '<f4'), ('f21', '<f4'), ('f22', '<i8'), ('f23', '<i8'), ('f24', '<f4'), ('f25', '<f4'), ('f26', '<f4')])


    .. note:: If we just want to obtain dtype from types, we only need to use\
    np.format_parser(formats=types, names=names, titles=titles).dtype
    """

    # If types is None, find types 
    if types is None:
        numrows, numcols = np.shape(stringarray)
        types = [] 
        for i in range(numcols):
            t = utils.guessarraytype(stringarray[:, i])
            types.append(t)

    if returndtype:
        dt = np.format_parser(formats=types, names=names, titles=titles).dtype
        return dt
    else:
        return types

def strarray2recarray(stringarray, names=None, types=None, titles=None):
    """
    stringarray2typedarray converts a 2D array of strings into a structured
    array. The datatypes may be guessed or supplied, and similarly names will
    be assigned as a prefix prepended to the column number starting from 0, 
    unless the names argument has been supplied.
    

    Parameters
    ----------
    stringarray: 2D `np.ndarray` of strings, mandatory
        input data
    names: list of strings, optional, defaults to `None`
        list of names of fields corresponding to stringarray
    types: list of variable types, optional, defaults to `None`
        types of variables corresponding to fields or columns of stringarray
    titles: list of strings, optional, defaults to `None`
        alias for names of fields, as required by `np.format_parser`


    Returns
    -------
    `np.recarray` or structured array


    Examples
    --------
    >>> fname = os.path.join(_here,'example_data/table_data.dat')
    >>> d = file2strarray(fname)
    >>> arrdtypes = arraydtypes(d)
    >>> x = strarray2recarray(d)
    >>> x.dtype == arrdtypes
    True
    >>> len(d) == len(x['f0'])
    True
    >>> x['f0'][0] == '6773'
    True
    >>> np.testing.assert_almost_equal(x['f1'][0], 0.089300)


    .. note:: names can be changed as long as all the fields are changed \
    simultaneously through `res.dtype.names = newnames`
    """
    numrows, numcols = np.shape(stringarray)

    arrdtypes = arraydtypes(stringarray, names=names, titles=titles,
                            types=types, returndtype=True)

    cols = []
    for i in range(numcols):
        t = np.array(stringarray[:, i], dtype=arrdtypes[i])
        cols.append(t)

    # Create tuple
    recs = zip(*cols)
    a = np.array(recs, dtype=arrdtypes)
    return a

if __name__ == '__main__':
    pass
    # fname = os.path.join(_here,'example_data/table_data.dat')
    # d = file2strarray(fname)
    # arrdtypes = arraydtypes(d)
    # x = strarray2recarray(d)
    # print x.dtype
