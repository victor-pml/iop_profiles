# -*- coding: utf-8 -*-
"""
Created on Tue Feb 10 13:08:49 2015

@author: vmv
"""
import numpy as np
from chauvenet import chauvenet

def qc_flags(wla,apd_ts_s,cpd_ts_int,bp,bbp,d_raw,t_raw,s_raw):
    #Quality control tests
     #1- spectra negative values between 400 and 675nm - negFlag = 1, spectra with nan index=nan and a 
     #negFlag=0 , so that spectra with missing data are not flagged as spectra with negative value
   wlngth = np.atleast_1d(wla)
   npackets = apd_ts_s.shape[1]
   # nwavelengths = apd.shape[2]
   negFlag = np.zeros([npackets])
  
   nonnegrange = np.intersect1d(np.where(wlngth>=400)[0],np.where(wlngth<680)[0])
     
   for i in range(npackets):
      test = next((index for index,value in enumerate(apd_ts_s[0,i,nonnegrange]) if value < 0), np.nan)
#      print test
      if np.isnan(test) == True:
         negFlagval= 0
      else:
         negFlagval= 1
          
      negFlag[i]=negFlagval
    
   apd_data_valid = [apd_ts_s[0][ind,:] for ind in range(npackets) if negFlag[ind]==0]
   cpd_data_valid = [cpd_ts_int[0][ind,:] for ind in range(npackets) if negFlag[ind]==0]
   bp_data_valid  = [bp[ind,:] for ind in range(npackets) if negFlag[ind]==0]
   bbp_data_valid = [bbp[0][ind,:] for ind in range(npackets) if negFlag[ind]==0]
   d_data_valid  = [d_raw[ind] for ind in range(npackets) if negFlag[ind]==0]
   t_data_valid  = [t_raw[ind] for ind in range(npackets) if negFlag[ind]==0]
   s_data_valid  = [s_raw[ind] for ind in range(npackets) if negFlag[ind]==0]
   #2 Quality control statistic -  chauvenet criteria on wavelength=400 nm
   #convert list to array
   testing_arr = np.asarray(apd_data_valid)
   filterchau = chauvenet(testing_arr[:,1]) #selecting wla[1] = 440, where spectra interruption occurs

   npackets2= len(apd_data_valid)

   apd_data_valid2 = [apd_data_valid[ind] for ind in range(npackets2) if filterchau[ind]==True]
   cpd_data_valid2 = [cpd_data_valid[ind] for ind in range(npackets2) if filterchau[ind]==True]
   bp_data_valid2 = [bp_data_valid[ind] for ind in range(npackets2) if filterchau[ind]==True]
   bbp_data_valid2 = [bbp_data_valid[ind] for ind in range(npackets2) if filterchau[ind]==True]
   d_data_valid2 = [d_data_valid[ind] for ind in range(npackets2) if filterchau[ind]==True]
   t_data_valid2 = [t_data_valid[ind] for ind in range(npackets2) if filterchau[ind]==True]
   s_data_valid2 = [s_data_valid[ind] for ind in range(npackets2) if filterchau[ind]==True]


   return apd_data_valid2,cpd_data_valid2, bp_data_valid2,bbp_data_valid2,d_data_valid2 ,t_data_valid2,s_data_valid2