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

from init_txt import initialisation_txt

import optics_routines as opt
import readingIOP_profiles as rd
#import opt_functions_ac as ac_f
#import opt_functions_bb3 as bb3_f
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

def iop_plotter_1file(ac_file,init_t_secs,output_folder,input_folder,summdir):
   '''Process a single .txt file, output with metadata and statistics'''

##########################CORE ROUTINE#######   
   
####Reading in the separate files
   
   fLines =rd._acsReadFile(ac_file)
   wla,wlc,dict_acsHeader,lines2parse =rd._acsHeaderParse(fLines)
   ms_acs,c_raw,a_raw, d_raw,t_raw,s_raw,bb_raw  = rd._acsDataParse(lines2parse,dict_acsHeader,wla,wlc)

  # ctd_file = files_mrg[1]
  # fLines_ctd =rd._ctdReadFile(ctd_file)
  # ms_ctd,t_raw,s_raw,d_raw =rd._ctdDataParse(fLines_ctd,ctd_col)

  # bb3_file = files_mrg[2]
  # fLines_bb3 = rd._bb3ReadFile(bb3_file)
  # ms_bb3,counts_raw,dark_raw = rd._bb3DataParse(fLines_bb3,bb3_col)
####End of reading######

###Processing the data####
### Merge the acs and CTD####
### after merging, T, Sal,depth and  counts are means and stddev at the same time scales as absorption and attenuation
#   t_mrg_mean,s_mrg_mean,d_mrg_mean,t_mrg_sd,s_mrg_sd,d_mrg_sd =rd._acsctdMerge(ms_acs,c_raw,a_raw,ms_ctd,t_raw,s_raw,d_raw)
### Merge the acs and bb####

 #  counts_mrg_mean,counts_mrg_sd =rd._acsbb3Merge(ms_acs,a_raw,ms_bb3,counts_raw)


### corrections of acs
  
  #attenuation
  #doing 
  #T and sal correction and 
  #water cal if available - not implemented in 26/01/2015 processing
 
# #ideally extracted from here >>>> tcal =  dict_acsHeader[0]['tcl']
# #done a bit brutally...
#   acs_cal['tcal'] = float(dict_acsHeader[0]['tcl'][7:11])
#   acs_cal['WAPver'] = dict_acsHeader[0]['ver'][53:58]

 # attenuation doing T&S correction  
  # cpd_ts = opt.opt_beam_attenuation(wlc, acs_cal,c_raw,t_mrg_mean, s_mrg_mean)
 # absorption doing T&S correction 
 # absorption doing scattering correction - By default using Zaneveld method
  # apd_ts_s,cpd_ts_int,bp = opt.opt_optical_absorption(wla,wlc,acs_cal,a_raw,cpd_ts,t_mrg_mean, s_mrg_mean,rwlngth=715.)
   
  # bbp = opt.opt_optical_backscattering(wla,apd_ts_s,counts_mrg_mean,counts_mrg_sd,bb3_cal,t_mrg_mean,s_mrg_mean)
   apd_ts_s = np.array(a_raw, ndmin=3)
   cpd_ts_int = np.array(c_raw, ndmin=3)
   bbp = np.array(bb_raw, ndmin=3) #bb is bbp (=bb-bbw)
   npackets = apd_ts_s.shape[1]
   nwavelengths = apd_ts_s.shape[2] 
   bp = np.zeros([npackets, nwavelengths])
   for ii in range(npackets):
       bp[ii,:] = cpd_ts_int[0][ii,:]- apd_ts_s[0][ii, :]
   time_real = ms_acs#[init_t_secs+ms/1000. for ms in ms_acs]

   apd_data_valid2,cpd_data_valid2, bp_data_valid2,bbp_data_valid2=qc_f.qc_flags(wla,apd_ts_s,cpd_ts_int,bp,bbp)

   
   iopstats =stats.dataStats(apd_data_valid2,cpd_data_valid2, bp_data_valid2,bbp_data_valid2,time_real,t_raw,s_raw,d_raw)      
    
   wr.writeOutputAll(summdir,acs_file,wla,bb3_cal,acs_cal,parameters,apd_ts_s,cpd_ts_int,bp,bbp,time_real,t_mrg_mean,s_mrg_mean,d_mrg_mean)
   
  # wr.summaryPlot(acs_file,apd_data_valid2,cpd_data_valid2, bp_data_valid2,bbp_data_valid2,time_real,t_mrg_mean,s_mrg_mean,d_mrg_mean,wla,bb3_cal,iopstats,summdir,saveplt=True)

   return apd_ts_s,cpd_ts_int,bp,bbp,time_real,t_mrg_mean,s_mrg_mean,d_mrg_mean,t_raw,s_raw,d_raw,wla,iopstats


def iop_plotter_1folder(input_folder,output_folder):
   '''for testing'''
   output_folder ='D:\\python_workspace\\profiles_iop\\output\\'
   input_folder='D:\\python_workspace\\profiles_iop\\input\\revised_optics\\'

   '''Get a list of files from the specified directory'''
   #newlist and py_init_times are lists of dictionaries

   txtFiles,txtDirs = initialisation_txt(input_folder,output_folder)
    # big loop for all files  for nn in range(len(newlist[archive_f_num])):
     #File name definitions
   timestr = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
   acbbbp_statsoutputfile = 'acbbbp_stats_'+timestr+'.csv' #stats for all a_pd and c_pd
   a_statsoutputplot = 'a_'+timestr+'.png' #stats for all a_pd and c_pd
   c_statsoutputplot = 'c_'+timestr+'.png' #stats for all a_pd and c_pd
   b_statsoutputplot = 'b_'+timestr+'.png' #stats for all a_pd and c_pd
   bb_statsoutputplot = 'bb_'+timestr+'.png' #stats for all a_pd and c_pd

   outputfilepath =  os.path.join(output_folder, acbbbp_statsoutputfile)
   outputfileplot_a = os.path.join(output_folder, a_statsoutputplot)
   outputfileplot_c = os.path.join(output_folder, c_statsoutputplot)
   outputfileplot_b = os.path.join(output_folder, b_statsoutputplot)
   outputfileplot_bb = os.path.join(output_folder, bb_statsoutputplot)
     
   fig_a = plt.figure("absorption")
   fig_c = plt.figure("attenuation")
   fig_b = plt.figure("scattering")
   fig_bb = plt.figure("backscattering")
   
   for nn in range(0,len(txtFiles)): #loop on the list of dictonaries of files with the same extension under the same directory
      
     
      ac_file = txtFiles[nn]
      txt_dir=txtDirs[nn]
      init_t_secs = 0.0
      apd_ts_s,cpd_ts_int,bp,bbp,time_real,t_mrg_mean,s_mrg_mean,d_mrg_mean,t_raw,s_raw,d_raw,wla,iopstats=iop_plotter_1file(ac_file,init_t_secs,output_folder,input_folder,txt_dir)   
       #Outputs
   #derived_statsoutputfile = 'derived_stats_'+timestr+'.csv' #stats bbp                         
      wr.writeOutputstats(ac_file,iopstats,output_folder,outputfilepath,parameters,bb3_cal,acs_cal,wla) #print out of median+IQR in 1 File
      wr.summarystatsPlot(wla,iopstats,bb3_cal,fig_a,fig_c,fig_b,fig_bb)#plot of all median
     # summaryPlot(rdatas,rstats,save=True,outputfolder=output_folder)
   fig_a.savefig(outputfileplot_a,dpi=150,format='png')
   plt.close("absorption")
   fig_c.savefig(outputfileplot_c,dpi=150,format='png')
   plt.close("attenuation")
   fig_b.savefig(outputfileplot_b,dpi=150,format='png')
   plt.close("scattering")
   fig_bb.savefig(outputfileplot_bb,dpi=150,format='png')
   plt.close("backscattering")
   


'''read the header and the data from one file'''

'''plot read data'''
'''save plots'''

'''calculate median and IQR profile'''
'''save median and IQR profile'''








