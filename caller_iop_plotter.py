# -*- coding: utf-8 -*-
"""
Created on Mon May 04 22:26:08 2015
rutine to read plot and save:
    -profiles of iop data
    -specra of iop data
@author: vmv
"""

import os
import datetime
import time
import numpy as np
import bisect

import matplotlib.pyplot as plt

from init import initialisation

import optics_routines as opt
import readingIOP as rd
import opt_functions_ac as ac_f
import opt_functions_bb3 as bb3_f
import opt_functions_qc as qc_f
import writingIOP as wr
import opt_stats as stats
import matplotlib.pyplot as plt

from utils import fill_value

#import inout_functions as io
__version__ = '20150505.01'

parameters = {}
parameters['Lat'] = fill_value
parameters['Lon'] = fill_value
parameters['Pro'] = 'MYOCEAN' # PRO==>project funding the data
parameters['pyver'] = __version__

bb3_cal={}
bb3_cal['wln']= [470.,532.,660.] #wavelengths specific for BB3-366
bb3_cal['S_f'] = [1.568e-05,1.119e-05,4.574e-06]
bb3_cal['drk'] = [57,54,54]
bb3_cal['pat'] = 0.0319 #pathlength for bb9 - in m
bb3_cal['units'] = '1/m'
bb3_cal['file'] ='tbd'
bb3_cal['datecal'] ='tbd' # date of cal/ WL wetlabs // or PML 

ac_cal={}
ac_cal['units'] = '1/m' 
ac_cal['file'] = 'tbd'
ac_cal['datecal'] = 'tbd'
ac_cal['Scorr'] = ''
ac_cal['tcal'] = fill_value
ac_cal['WAPver'] = ''
ctd_col= {}
ctd_col['time']=0
ctd_col['temp']=0
ctd_col['dept']=2
ctd_col['sali']=3

bb3_col={}
bb3_col['time'] = 0 #in file
bb3_col['coun'] = [4,6,8] #in file
bb3_col['dark'] = 9 #in file




'''Get a list of files from the specified directory'''

'''read the header and the data from one file'''

'''plot read data'''
'''save plots'''

'''calculate median and IQR profile'''
'''save median and IQR profile'''








