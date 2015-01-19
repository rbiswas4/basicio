#!/usr/bin/env python

import numpy as np
import os.path
import cStringIO
from basicio import utils
import os

_here  = os.path.dirname(os.path.realpath(__file__))

def file2numpyarray(file, buffer=False, datastring=None):
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
    >>> d = file2numpyarray(fname)
    >>> type(d)
    np.ndarray


    .. note:: 1. Cofirmation of buffer was introduced in order to prevent \
            errors where an incorrect filename passed was interpreted as a \
            buffer.

    """

    if os.path.isfile(file):
        # print 'This is a filename'
        fp = open(file)
    else:
        # print 'this is a string'
        # Confirm
        if not buffer:
            raise ValueError('The file does not exist, and buffer is False,\
                    so cannot iterpret as data stream')
        fp = cStringIO.StringIO(file)

    line = fp.readline()
    data = []
    while line != '':
        if datastring is not None:
            if not line.startswith(datastring):
                continue
        lst = utils.tokenizeline(line)[0]
        data.append(lst)
        line = fp.readline()

    fp.close
    data = np.asarray(data)
    return data
# r=np.core.records.fromrecords([(456,'dbe',1.2),(2,'de',1.3)],
#          ... names='col1,col2,col3')
