# -*- coding: utf-8 -*-
"""
Created on Tue Jan 27 17:43:38 2015

@author: vmv
"""

#bb3_time_col = 0 #in file
#bb3_coun_col = [4,6,8] #in file
#bb3_dark_col = 9 #in file
import numpy as np

###ALL reading routines
####################acs routines##############################
# testing Loop through the selected files to read raw data into arrays
# move out of here
def _acsReadFile(ff):
   '''open acs file (from Wetlabs WAP), return list of stripped lines'''
  # ff=acs_file#for debbugging 
   with open(ff,'r') as f:
       fLines = f.readlines()
   return fLines
# testing Loop through the selected files to read raw data into arrays
# move out of here   
def _acsHeaderParse(fLines):
   '''fill header dict with info from the L2S header lines'''
   acsHeader=[]
   dict_acsHeader = []
 #  headsep = ','
   llind = 0
   ll = fLines[llind]
   test = ll.strip().split('\t')
   test = ll.split(',')
   wlc = [412.,440.,488.,510.,532.,555.,650.,715.]
   wla = wlc
   #[float(val.split('c')[1]) for val in test if val.startswith('c')]
   #wla = [float(val.split('a')[1]) for val in test if val.startswith('a')]
 
#   while not ll.startswith('Lat')  :
# #     print ll
#      headline = ll.split(headsep,1)
#   acsHeader.append(headline[0].strip())
  
#   dict_acsHeader.append(dict(ver=acsHeader[0],srn=acsHeader[2],\
#                        tcl=acsHeader[4],ptl=acsHeader[7],\
#                        wln=float(acsHeader[8])))
 
   
   lines2parse = fLines [llind+1::]
   return wla,wlc,dict_acsHeader,lines2parse
 # testing Loop through the selected files to read raw data into arrays
# move out of here  
def _acsDataParse(lines2parse,dict_acsHeader,wla,wlc):
   '''fill header dict with info from the L2S header lines'''
   ms_acs = []
   c_raw = []
   a_raw = []
   t_raw = []
   bb_raw = []
   s_raw = []
   d_raw =[]
   wln = 9  #int(dict_acsHeader[0]['wln'])
   for ll in lines2parse:
      vals = [float(val) for val in ll.strip().split(',')]
      ms_acs.append(vals[2])
      d_raw.append (vals[3])
      a_raw.append(vals[4:13])
      c_raw.append(vals[13:22])
      bb_raw.append(vals[22:25])
      t_raw.append(vals[25])
      s_raw.append(vals[26])
   return ms_acs,c_raw,a_raw, d_raw,t_raw,s_raw,bb_raw 
   #plot(ms_acs,[c[10] for c in c_raw])
####################acs routines##############################
####################ctd routines#############################
def _ctdReadFile(ff):
   '''open ctd file (from WAP), return list of stripped lines'''
#   ff=ctd_file #for debbugging

   with open(ff,'r') as f:
      fLines_ctd = f.readlines()
   return fLines_ctd
    
def _ctdDataParse(lines2parse,ctd_col):
#defined globally, remove when necessary   
#   lines2parse=fLines_ctd ##for debbugging remove to run
   ms_ctd = []
   data_ctd =[]
   t_raw = []
   s_raw = []
   d_raw =[]
   for ll in lines2parse[1::]:
      vals = [val for val in ll.strip().split('\t')]
      ms_ctd.append(float(vals[ctd_col['time']]))
      data_ctd.append(vals[1])
   for ll in data_ctd:
      vals = [float(val) for val in ll.strip().split(',')]
      t_raw.append(vals[ctd_col['temp']])
      s_raw.append(vals[ctd_col['sali']])
      d_raw.append(vals[ctd_col['dept']])
   return ms_ctd,t_raw,s_raw,d_raw 
####################ctd routines#############################    

####################bb3 routines#############################
def _bb3ReadFile(ff):
#   ff = bb3_file #value for debbugging remove for running
   '''open ctd file (from WAP), return list of stripped lines'''
   with open(ff,'r') as f:
      fLines_bb3 = f.readlines()
   return fLines_bb3
    
def _bb3DataParse(lines2parse,bb3_col):
#   lines2parse = fLines_bb3 #for debbugging , remove for running 
 
   ms_bb3 = []
   counts_raw = []
   dark_raw = []
  
   for ll in lines2parse:
      vals = [val for val in ll.strip().split('\t')]
      ms_bb3.append(float(vals[bb3_col['time']]))
      counts_raw.append([int(vals[i]) for i in bb3_col['coun']])
      dark_raw.append(int(vals[bb3_col['dark']]))
     #plot(ms_bb3,[c[0] for c in counts_raw])

   return ms_bb3,counts_raw,dark_raw 


####################bb3 routines#############################    

def _acsctdMerge(ms_acs,c_raw,a_raw,ms_ctd,t_raw,s_raw,d_raw):
   #crude routine to find minimum ms differences around acs times for ctd
   #take one value of ms_acs
   t_mrg_mean = []
   t_mrg_sd = []
   s_mrg_mean = []
   s_mrg_sd = []
   d_mrg_mean = []
   d_mrg_sd =[]   
   counter=0
   for acs_t in ms_acs:
    #  print acs_t,counter
      difflist = []
  #    finaldifflist = []
      difflist = abs(np.array(ms_ctd)-acs_t)
      difzip = zip(difflist,range(len(difflist)))
      difinds = [ind for msdif,ind in difzip if msdif<=2500]
      
      if len(difinds)==0:
          t_mrg_mean.append(np.nan)
          t_mrg_sd.append(np.nan)
          s_mrg_mean.append(np.nan)
          s_mrg_sd.append(np.nan)
          d_mrg_mean.append(np.nan)
          d_mrg_sd.append(np.nan)
          #add the rest
      else:
         try:         
            t_selected = t_raw[min(difinds):max(difinds)]
            t_mrg_mean.append(np.nanmean(t_selected))
            t_mrg_sd.append(np.std(t_selected))
            s_selected = s_raw[min(difinds):max(difinds)]
            s_mrg_mean.append(np.nanmean(s_selected))
            s_mrg_sd.append(np.std(s_selected))
            d_selected = d_raw[min(difinds):max(difinds)]
            d_mrg_mean.append(np.nanmean(d_selected))
            d_mrg_sd.append(np.std(d_selected))
         except:
            t_mrg_mean.append(np.nan)
            t_mrg_sd.append(np.nan)
            s_mrg_mean.append(np.nan)
            s_mrg_sd.append(np.nan) 
            d_mrg_mean.append(np.nan)
            d_mrg_sd.append(np.nan)
 #     print difinds
      counter+=1
    #  print, len(ms_acs),len(t_mrg_mean) #should be the same                       
    # plot(ms_ctd,[t for t in t_raw],'ob')  
    #find an array of values in ms_ctd that are +/1 second
   return t_mrg_mean,s_mrg_mean,d_mrg_mean,t_mrg_sd,s_mrg_sd,d_mrg_sd
   
def _acsbb3Merge(ms_acs,a_raw,ms_bb3,counts_raw):
   #crude routine to find minimum ms differences around acs times for ctd
   #take one value of ms_acs
   counts_mrg_mean = []
   counts_mrg_sd = []
   ms_bb_arr=np.atleast_1d(ms_bb3)
   counts_raw_arr=np.array(counts_raw,ndmin=3)

   

   counter=0
   for acs_t in ms_acs:
    #  print acs_t,counter
      difflist = []
  #    finaldifflist = []
      difflist = abs(ms_bb_arr-acs_t)
      difzip = zip(difflist,range(len(difflist)))
      difinds = [ind for msdif,ind in difzip if msdif<=2000]
      
      if len(difinds)==0:
          counts_mrg_mean.append(np.nan)
          counts_mrg_sd.append(np.nan)

          #add the rest
      else:
         try:         
            counts_selected_b = counts_raw_arr[0,[difinds],0]
            counts_selected_g = counts_raw_arr[0,[difinds],1]
            counts_selected_r = counts_raw_arr[0,[difinds],2]
            counts_mrg_mean.append([np.nanmean(counts_selected_b),np.nanmean(counts_selected_g),np.nanmean(counts_selected_r)])
            counts_mrg_sd.append([np.std(counts_selected_b),np.std(counts_selected_g),np.std(counts_selected_r)])
     
         except:
            counts_mrg_mean.append(np.nan)
            counts_mrg_sd.append(np.nan)         
#      print difinds
      counter+=1
    #  print, len(ms_acs),len(t_mrg_mean) #should be the same                       
    # plot(ms_ctd,[t for t in t_raw],'ob')  
    #find an array of values in ms_ctd that are +/1
   return counts_mrg_mean,counts_mrg_sd







