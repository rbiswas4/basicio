#!/usr/bin/env python

import numpy as np
import os.path
import cStringIO
from basicio import utils

def loadtable(file ):


    if os.path.isfile(file):
        # print 'This is a filename'
        fp  = open(file)
    else:
        # print 'this is a string'
        fp =  cStringIO.StringIO(file)


    line = fp.readline()
    data = [] 
    while line !='':
        lst = utils.tokenizeline(line)[0]
        data.append(lst)
        line = fp.readline()

    fp.close
    data = np.asarray(data)
    return data



        
# r=np.core.records.fromrecords([(456,'dbe',1.2),(2,'de',1.3)],
#          ... names='col1,col2,col3')
