# -*- coding: utf-8 -*-
"""
Created on 14/01/2015 pm
main envelope for plotting iop profiles
@author: vmv
"""

import caller_iop_plotter as caller_iop
import matplotlib.pyplot as plt

#import csv
#import numpy as np
#def main():
plt.close('all')
#input_folder='J:\\python_workspace\\globolakes_iop\\input\\'
#def main():
#dates = ['09072014\\','14072014\\','15072014\\','16072014\\','17072014\\','18072014\\','19072014\\','24072014\\','25072014\\']
#dates = ['test\\']#,'st001\\','st002\\','st004\\','st006\\','st007\\']
#dates = ['st002']
output_folder ='D:\\python_workspace\\profiles_iop\\output\\'

#output_folder ='J:\\opticsdatabasev00\\globolakes\\2014\\ACS\\geneva\\proc_v_20150224\\'
#for ndir in range(0,len(dates)):
#   input_folder='J:\\opticsdatabasev00\\globolakes\\2014\\ACS\\geneva\\'+dates[ndir]
'''Definition of input file'''
input_folder='D:\\python_workspace\\profiles_iop\\input\\revised_optics\\'
  
   #output_folder = 'J:\\opticsdatabasev00\\globolakes\\2014\\ACS\\balaton\\'+dates[ndir]
print input_folder
print output_folder

caller_iop.iop_plotter_1folder(input_folder,output_folder)#,\
 #  quiet=False,wlpars=[400,750,3.3])
  
#   filename = 'J:\\python_workspace\\globolakes_iop\\input\\archive_pair_02.000'
#   print filename   
#   data_L0 = np.genfromtxt(filename,comments=None, delimiter=',')   
#   print type(data_L0) 
#   row,col = data_L0.shape 
#if __name__ == "__main__":
#    main()
