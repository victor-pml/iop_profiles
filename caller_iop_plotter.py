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
import opt_functions_acs as acs_f
import opt_functions_bb3 as bb3_f
import opt_functions_qc as qc_f
import writingIOP as wr
import opt_stats as stats
import matplotlib.pyplot as plt

from utils import fill_value

#import inout_functions as io
__version__ = '20150224.01'
