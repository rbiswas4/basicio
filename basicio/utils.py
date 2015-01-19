#!/usr/bin/env python

import numpy as np
import sys
# import string

__all__ = ['tokenizeline', 'guesstype', 'guessarraytype']


def tokenizeline(line, delimitter="", ignorestrings="#", prependstring=None,
                 format='list'):
    """
    splits the string line into two substrings before and after the
    first instance of a string in the list ignorestrings, and returns
    a tuple of a list/tuple of tokens obtained by tokenizing the first
    substring on the delimiter delimitter and the second substring.

    Parameters
    ----------
    line: mandatory, string
        string to tokenize
    delimitter: optional, defaults to ""
        string of characters (other than whitespace) to
        be used as a delimiter for tokenizing the line.
        for example  in the case of a line of TSV, it would be "\t"
    ignorestrings: string, optional, defaults to "#"
        string, after which the remainder of the line will be ignored
        in the list of tokens
    prependstring: string, optional defaults to None
        if not None, assumes  desired data is prepended by prependstring, and
        removes this prepended string
    format: string, optional defaults to 'list'
        describes the format of the collection of tokens and can be either
        'list' or 'tuple'

    Returns
    -------
    tuple: (lst, list of metadata)
        lst is a list/tuple of token strings, list of metadata strings


    Examples
    --------
    >>> myline = "KJAHS KH AKJHS jjhJH. JH HJ   JHH JH #tests "
    >>> tokenizeline(myline, delimitter=".")
    (['KJAHS KH AKJHS jjhJH', ' JH HJ   JHH JH'], ['tests'])
    >>> tokenizeline(myline, delimitter="")
    (['KJAHS', 'KH', 'AKJHS', 'jjhJH.', 'JH', 'HJ', 'JHH', 'JH'], ['tests'])
    >>> myline = "data KJAHS KH AKJHS jjhJH. JH HJ   JHH JH #tests "
    >>> tokenizeline(myline, delimitter="", prependstring='data')
    (['KJAHS', 'KH', 'AKJHS', 'jjhJH.', 'JH', 'HJ', 'JHH', 'JH'], ['tests'])


    .. note::  slightly diff signature from _tokenizeline which seemed to be  \
    too complicated and is done more simply here, as the metadata is captured \
    as a list rather than a comment string.
    TODO: allow multiple delimiter strings.
    """
    line = line.strip()

    # Find comments to ignore
    lst = line.split(ignorestrings)
    commentlist = lst[1:]
    linelst = lst[0]
    if prependstring is not None:
        linelst = linelst.lstrip(prependstring)
    linelst = linelst.strip()

    if delimitter == '':
        tokens = linelst.split()
    else:
        tokens = linelst.split(delimitter)
    if format == 'tuple':
        tokens = tuple(tokens)
    return (tokens, commentlist)


def guesstype(s, makeintfloats=False):
    """
    guess the datatype (between ints, floats, str) of the object printed
    as a string and return a tuple of (dtype, data in appropriate dtype)

    Parameters
    ----------
    s : mandatory, string
        elemental python data type whose type we want to obtain

    makeintfloats: optional, bool, defaults to False
        forces integers to float (f4)


    Returns
    -------
    tuple: (dtype, sprime)
        where sprime is the data represented by the string in its
        appropriate datatype.


    Examples
    --------
    >>> s = '123'
    >>> guesstype(s)
    ('i8', 123)
    >>> guesstype(s, makeintfloats=True)
    ('f4', 123.0)
    >>> guesstype('12.3')
    ('f4', 12.3)
    >>> guesstype('s23')
    ('a20', 's23')
    """
    try:
        int(s)
        if makeintfloats:
            return 'f4', float(s)
        else:
            return 'i8', int(s)
    except ValueError:
        pass
    try:
        float(s)
        return 'f4', float(s)
    except ValueError:
        pass
    return "a20", s


def guessarraytype(arr, makeintfloats=False):
    """
    guess the underlying datatype (out of 'i8', 'f4', 'a20') of an iterable
    of strings. If the iterable contains strings that are guessed to be of
    different types, the most 'general' type will be returned, where we mean
    ('i8', 'f4', 'a20') are assumed to be in increasing order of generality.


    Parameters
    ----------
    iterable : mandatory, array-like object of strings
        collection of strings
    makeintfloats: optional, bool, defaults to False
        If true, assumes that strings that can be integers are actually
        floats, so that strings like '3' are treated as '3.0'


    Returns
    -------
    One of 'i8', 'f4', 'a20'


    Examples
    --------
    >>> arr = ['3', '2', '4']
    >>> guessarraytype(arr)
    'i8'
    >>> arr = ['3', '2', '4']
    >>> guessarraytype(arr, makeintfloats=True)
    'f4'
    >>> arr = ['3', '2', '4', '7.0']
    >>> guessarraytype(arr, makeintfloats=False)
    'f4'
    >>> arr = ['3.4', '2.7', '4.0']
    >>> guessarraytype(arr)
    'f4'
    >>> arr = ['3.4', '2.7', '4.0', 's23']
    >>> guessarraytype(arr)
    'a20'
    """
    typearr = np.array(map(lambda x: guesstype(x,
                       makeintfloats=makeintfloats)[0], arr))
    if any(typearr == 'a20'):
        return 'a20'
    elif any(typearr == 'f4'):
        return 'f4'
    elif all(typearr == 'i8'):
        return 'i8'
    else:
        raise ValueError('It seems that guesstype is not finding one of \
            \'f4\', \'i8\' or \'a20\' as the types of all elements in arr')
        sys.exit()


def _tokenizeline(line, delimstrings=" ", ignorestrings=["#"]):
    """
    splits the string line into two substrings before and after the 
    first instance of a string in the list ignorestrings, and returns
    a tuple of a list of tokens obtained by tokenizing the first 
    substring on the delimiter delimstrings and the second substring.

    Parameters
    ----------
    line: mandatory, string 
        string to tokenize
    delimstrings: optional, defaults to ""
        string of characters (other than whitespace) to 
        be used as a delimiter for tokenizing the line. 
        for example  in the case of a line of TSV, it would be "\t"
    ignorestrings: optional, defaults to ["#"]
        list of strings, occurances of any of which in a
        line indicates the remainder of the line is a
        comment which should not be tokenized

    Returns
    -------
    tuple: list of token strings, string of comments

    Examples
    --------

    >>> myline = "KJAHS KH AKJHS jjhJH. JH HJ   JHH JH #tests "
    >>> _tokenizeline(myline, delimstrings=".")
    (['KJAHS KH AKJHS jjhJH', 'JH HJ   JHH JH'], '#tests')
    >>> _tokenizeline(myline, delimstrings="")
    (['KJAHS', 'KH', 'AKJHS', 'jjhJH.', 'JH', 'HJ', 'JHH', 'JH'], '#tests')

    ..notes:
        status: Will not be using, trying to use tokenizeline instead
        Sat Jan 17 18:20:54 PST 2015
            Tested, seems to work correctly,
            testio.py
            #Section: Test tokenization:
            R. Biswas, July 17, 2012
            Rewritten to work for multiple ignorestrings in list to fix bug,
            R. Biswas, Sep 15, 2012
        TODO: allow multiple delimiter strings. 
    """    
    tokens=[]
    comments = ''

    tmp = line.strip()
    if tmp: 
        minlengthforst = -1
        actualignorestring = None
        lengthofline = len(tmp)

            #Find the ignore string that occurs first

        for st in ignorestrings:
            linelist = tmp.split(st)
            lengthforst = len(linelist[0])
            if lengthforst  < lengthofline:

            #These strings are on the line
                if lengthforst < minlengthforst or -1 == minlengthforst:
                    actualignorestring = st
                    minlengthforst = lengthforst 

        tokstring = ""

        if actualignorestring:    
            linelist = tmp.split(actualignorestring)
            if len(linelist[1])>1:
                comments = actualignorestring + actualignorestring.join(linelist[1:])
            tokstring = linelist[0]
        else:
            tokstring = tmp
        if delimstrings== "":
            tokens = tokstring.split()
        else:
            #print "delimstring " , delimstrings
            tokens = map(lambda x: x.strip(), tokstring.split(delimstrings))
    ret = ( tokens , comments)
    return ret

def builddict(fname,
    ignorestrings=['#'],
    dictdelim='=',
    startblock = None, 
    endblock =None):

    """builddict (fname) reads in the file with filename
    fname, and builds a dictionary of keys vs values from
    it
    args: 
        fname:    mandatory, string 
            filename from which the dictionary is to be built
        ignorestring: optional, string, defaults to ["#"]
            list of strings, after which the remaining part of 
            the line should be ignored. 
        dictdelim: optional, string, defaults to '='
            delimiter used to separate keys, values
            in building the dictionary
        startblock = optional, string, defaults to None
            Can do a replace within only the starting and ending
            blocks but both must be provided. These blocks can 
            start with a comment string 
        endblock = string, optional, defaults to None
            Can do a replace within only the starting and ending
            blocks but both must be provided. These blocks can 
            start with a comment string 
    returns:
        dictionary of keys and values (in strings)
    example usage :
        builddict ( fname)  
    status: 
        Seems to work correctly, tested on CAMB params.ini,
        R. Biswas, July 08, 2012 
        That was in configdict. Rewritten to use ioutilst, not tested 
        yet,
        R. Biswas, Aug 09, 2012
    """
    f = open(fname, "r")
    line = f.readline()
    i = 0
    
    #print ignorestrings
    paramdict={}
    readin = False
    while line != '': 
        if startblock: 
            if (readin ==False):
                if line.find(startblock) !=-1:
                    readin = True
        else:
            readin  =True
        if readin == False:
            line = f.readline()
            continue    
    #while line != '':
        tmp = tokenizeline(line, ignorestrings = ignorestrings , 
            delimstrings = dictdelim)
        
        #print line , tmp
        tmp = tmp[0]
        if len(tmp) >1:
                key = tmp[0].strip()
                #print key, tmp
                val = tmp[1].strip()
                paramdict[str(key)] = str(val)  
        line=f.readline()
        if endblock and line.find(endblock) !=-1:
            readin = False
            #print "FOUND ENDBLOCK"
            continue
    
    f.close()
    return paramdict
def loadfile2array(fname, 
    datastrings = [],
    datadelims = "",
    ignorestrings = ["#"], 
    ignorelines = [],
    ignorecols = [] , 
    usecols = [],
    usecoldicts = [],
    validatetable = True,
    converttofloat =False,
    keys = None ,
    makeintfloats = False,
    verbose = False,
    extension =''):

    """loadfiletoarray loads a (part) of a ASCII file to a list or a 
    numpy array.
    args:
        fname:         mandatory , string 
            name of file which is to be read
            eg. "FITOPT001.FITRES
        datastrings:     optional, list of strings, defaults to []
            if not an empty list, contains strings with which 
            the lines containing data to be turned into a np
            array. 
        datadelims:    optional, string, defaults to ""
            if equal to "" (default) the data delimiters are 
            assumed to be whitespace. Otherwise this string
            has to be specified (eg for a CSV)
        ignorelines: optional, list of integers, defaults to []
            list of file linenumbers on the file which will be 
            ignored. These linenumbers start from 1 and match
            the line numbers shown by vi 
        ignorestrings:     optional, list of strings, defaults to []
            if not an empyty list, contains strings after which
            a line will not be read in
        usecols:    optional, list of integers, defaults to []
            only load these cols into the array
        ignorecols:     optional, list of integers, defaults to []
            do not load these cols into the array.
        NB: It is expected that none or only one of 
            usecols, and ignorecols will be used     
        usecoldicts:    optional, list of integers , defaults to  []
            col number of a set of strings that could be used 
            to identify the row
        validatetable: optional, defaults to True
            if True, checks that the number of elements in mylist 
            for each row is the same. On success it returns a return
            code of 0, else a return code of 1
        converttofloat:    optional, defaults to False
            if True, then it converts the Table to a numpy 
                array of floats
            if False, the it leaves the table as a list of strings
        verbose:
            optional, bool, defaults to False
            if True, turns on vmode, printing out messages.
        extension:    optional, defaults to ""
            if 'gz', uses the gzip library to open gzipped files
    returns:
        tuple
            if converttofloat == True, 
                (numpy structued 2D array , list of strings, 
                returncode ) 
            else , 
                (list of list of strings , 
                empty list of strings , returncode)

            returncode = 0 , everything checked out
                   = 1 , terrible failure
            
            I PLAN TO KEEP returncode AS THE LAST ENTRY
            OF THE TUPLE, R. Biswas, July 18, 2012
    example usage:
        (data , dictlist , returncode) = 
            io.loadfiletoarray("FITOPT001.FITRES",
            datastrings=["SN"],
            ignorecols=[0,1], 
            converttofloat=True, 
            usecoldicts = [0,1])
    status:
        tested using testio.py
        Most features seem to work
            R. Biswas, July 18, 2012
        updated this routine to put in a real coldict. Have no idea
        why I wrote the return values the way they were. Got rid of 
        dictlist and have a col. I don't see the point of having 
        multiple values in the dictionary
            R. Biswas, Aug 11,2012
        rewritten from loadfiletoarray to use a numpy structured array
            R. Biswas,  Mon Mar 25 00:31:47 CDT 2013
        Fixed bug that arose when a column had inconsistent types, eg.
            starting with int but then incorporating strings (as in
            cids) by looking at the entire column.
            R. Biswas, Mon Mar 25 09:06:14 CDT 2013
    """
    import numpy as np
    import gzip

    vmode = False
    if verbose :
        vmode = True
    if extension=="":
        f = open(fname,"r")
    elif extension == "gz":
        f = gzip.open(fname,"rb")
    else:
        "Don't know what this extension is"
        return 1
    line = f.readline()
    linenum  = 1 

    mylist = []

    numelems = 0 #Number of elements in each row of the list    
    numtokens = 0
    if vmode:
        print "INPUTS "
        print "datastrings", "usecols", "ignorecols"
        print datastrings, usecols , ignorecols , "\n" 
    while line!="":
        if verbose:
            print 'iterating line loop'
        tokens = []
        newtoken = False
        currentline = line
        line = f.readline() #CHECK
        linenum +=1
        if vmode:
            print "Linenum = ", linenum
            print "corresponding line = ", currentline +"\n"
    
            # Leave out lines that we don't want
        if linenum in ignorelines:
            if vmode:
                print "Ignoring line ", currentline, "in ignorelines ", ignorelines
            continue
        if any(map(lambda x: currentline.startswith(x),ignorestrings)):
            if vmode:
                print "Ignoring line ", currentline, "starting with ignorestrings ", ignorestrings
            continue
            #If there is a datastring
        if len(datastrings)==0:
#orig            tokens , comments = tokenizeline (currentline, 
            tokens , comments = tokenizeline (currentline, 
                    ignorestrings = ignorestrings,
                    delimstrings =  datadelims)
            newtoken = True
            numtokens = len(tokens)
            if vmode:
                print "in  line no "+ linenum + numtokens +"tokens were found" 
        elif any(map(lambda x: currentline.startswith(x), datastrings)):
            # orig            tokens, comments = tokenizeline (currentline,
            tokens, comments = tokenizeline(currentline,
                                            ignorestrings=ignorestrings,
                                            delimstrings=datadelims)
            if vmode:
                print "current line ", currentline + " tokenized to ", tokens
            newtoken = True
            numtokens = len(tokens)
        else:
            pass
        if validatetable:
            if numelems == 0:
                numelems = numtokens
            if numelems != numtokens:
                return ([], [], 1)

        if newtoken:
            if vmode:
                print "new tokens found of length", len(tokens)
                print "These tokens are ", tokens
            if len(tokens) > 0:
                mylist.append(tokens)
        # line = f.readline()
        # print line , "\n", tokens
        if verbose:
            print "mylist now of length ", len(mylist)
            print "mylist = ", mylist

    f.close()

    if vmode:
        print "printing mylist[0]"
        print mylist[0]
    cutlist = []
    dictlist = []
    coldict = {}

    # ##Choose Columns for list
    if len(ignorecols) > 0:
        usecols = [i for i in range(len(mylist[0])) if i not in ignorecols]
    if vmode:
        print len(mylist[0])
        print len(usecols)
    cutlistiter = 0
    if (len(usecols) < len(mylist[0])) and (len(usecols) != 0):
        for row in mylist:
            cutrow = [row[i] for i in range(len(row)) if i in usecols]
            cutlist.append(cutrow)
            # print usecoldicts
            if len(usecoldicts) > 0:
                dictrow = [row[i] for i in range(len(row)) if i in usecoldicts]
                dictlist.append(dictrow)
                coldict[dictrow[0]] = cutlistiter

            cutlistiter += 1
    else:
        cutlist = mylist
        # ## Assuming things can be turned into floats
    if converttofloat:
        # # Check the data types of 1st row
        types = getdatatypes(cutlist, keys=keys, makeintfloats=makeintfloats)
        # print types
        # print cutlist
        # print len(cutlist)
        cutarray = np.zeros(len(cutlist), dtype=types)
        # print len(cutarray)
        for i in range(len(cutlist)):
            # map(float, cutlist[i])
            # cutarray[i] = np.array(map(float,cutlist[i]))
            # print len(cutlist)
            cutarray[i] = tuple(cutlist[i])
            # print i, len(cutlist[i]), len(cutarray[i])
            # print cutlist[i]
            # print cutarray[i]
        # print "length of array ", len(cutarray)
        # return (cutarray ,dictlist , 0 )
        return (cutarray, coldict, 0)
    # return (cutlist , dictlist , 0 )
    return (cutlist, coldict, 0)
