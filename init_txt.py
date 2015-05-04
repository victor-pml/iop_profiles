# -*- coding: utf-8 -*-
"""
Created on Tue Jan 27 17:48:28 2015
modif May 04 22:59:00 2015

@author: vmv
"""
import os
import time
import numpy as np
import bisect
from glob import glob
import fnmatch



def initialisation_txt(input_folder,output_folder):
   input_folder='D:\\python_workspace\\profiles_iop\\input\\revised_optics\\'
   output_folder ='D:\\python_workspace\\profiles_iop\\output\\'
   '''when debugging load up these defaults to get started quickly'''
   txtFiles = []
   txtDirs = []
   search_txtfile = 'WCO*'   
   
   for root,dirnames,filenames in os.walk(input_folder):
      for filename in fnmatch.filter(filenames,search_txtfile):
         txtFiles.append(os.path.join(root,filename))    
         txtDirs.append(root)

   
   return txtFiles,txtDirs #a list of dictionaries