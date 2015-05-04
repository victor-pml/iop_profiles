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



def initialisation(input_folder,output_folder):
  #input_folder='D:\\python_workspace\\profiles_iop\\input\\revised_optics\\'
  # output_folder ='D:\\python_workspace\\profiles_iop\\output\\'
   '''when debugging load up these defaults to get started quickly'''
   #fileListRaw = os.listdir(input_folder)
 #  search_file = 'archive_pair_02.*'
 #  pair02Files = [y for x in os.walk(input_folder) for y in glob(os.path.join(x[0], search_file))]
   #[os.path.join(input_folder,f) for f in fileListRaw if search_file in f]
   search_summfile = 'Summary.*'
   summFiles = []
   summdirs = []
   search_battfile = 'Battery.*'
   battFiles = []
   search_mrgfile = 'archive_MRG.*'
   mrgFiles = []
   
   txtFiles = []
   txtdirs = []
   search_txtfile = 'WCO*'   
   
   for root,dirnames,filenames in os.walk(input_folder):
      for filename in fnmatch.filter(filenames,search_txtfile):
         txtfiles.append(os.path.join(root,filename))    
         txtdirs.append(root)
   
   
   for root, dirnames, filenames in os.walk(input_folder):
      for filename in fnmatch.filter(filenames, search_summfile):
         summFiles.append(os.path.join(root, filename))
         summdirs.append(root)
         
      for filename in fnmatch.filter(filenames, search_battfile):
         battFiles.append(os.path.join(root, filename))
      
      for filename in fnmatch.filter(filenames, search_mrgfile):
         mrgFiles.append(os.path.join(root, filename))         

   #[os.path.join(input_folder,f) for f in fileListRaw  if search_summfile in f]
       #L2sFiles = [os.path.join(inputfolder,f) for f in fileListRaw if search_file in fileListRaw]
  
  # battFiles = [y for x in os.walk(input_folder) for y in glob(os.path.join(x[0], search_battfile))]
   #[os.path.join(input_folder,f) for f in fileListRaw  if search_battfile in f]
   #search_mrgfile = 'archive_MRG.*'
  # mrgFiles = [y for x in os.walk(input_folder) for y in glob(os.path.join(x[0], search_mrgfile))]
   #[os.path.join(input_folder,f) for f in fileListRaw  if search_mrgfile in f]
   
   
   newlist = []
   py_init_times = []
   #test=[]
   batFile=[]
   mrgFile=[]
   for summfile in summFiles:
      summdir_iter,filed =os.path.split(summfile)
      summdir_iter=summdir_iter+'\\'
      ext = summfile.split('.')[-1]      
      for root, dirnames, filenames in os.walk(summdir_iter):
     #   print filenames
     #    print ext     
         for filename in fnmatch.filter(filenames, 'Battery.'+ext):
            batFile.append(os.path.join(summdir_iter, filename))
         for filename in fnmatch.filter(filenames, 'archive_MRG.'+ext):
            mrgFile.append(os.path.join(summdir_iter, filename))
      
         #batFile = [bf for bf in battFiles if bf.endswith(ext)]
         #mrgFile= [bf for bf in mrgFiles if bf.endswith(ext)]
   for ii in range(len(summFiles)):
      newlist.append(dict(sumf=summFiles[ii],bat=batFile[ii],mrg=mrgFile[ii]))
          
          
   for n in newlist: #cycle through list
    #  for key in n.keys(): #cycle through keys of the dict
    #     print key, n[key] #print the key and its value
      ff= n['bat']       
        # firstdict = n[key]
        # ff = firstdict['bat']
      with open(ff,'r') as f:
         fLines = f.readlines()
         header = fLines[0].strip().split('\t')
       #  flt_ms_start = float(header[0].split()[0])
         header1 = header[0]
         str_time_date_start = header1.split()[-1]+' '+header[-1]
         py_time_start = time.strptime(str_time_date_start, "%H:%M:%S %m/%d/%y")
         py_init_times.append(dict(batf=ff,initime=py_time_start))
   #testing to read MRG files for finding out the address of files to be read
 
   
   return newlist,py_init_times,summdirs #a list of dictionaries