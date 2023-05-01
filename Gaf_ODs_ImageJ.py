#!/usr/bin/python

#For caluclating optical density (OD), or absorbance, from Gafchromic film scanned with the Epson scanner and processed with imageJ
#Takes the csv output from ImageJ ROI's and returns a second csv file containing %transmitance  and OD values
#OD is calculated using the relationship 'OD = 2-log(%T)'


import pandas as pd
import numpy as n
from datetime import date

x = str(input("ImageJ ROI file = "))
y = float(input("Max transmission value = "))

def OD(file,max_trans):
     
    data = pd.read_csv(file)
    data['%T'] = (data['Mean']/max_trans)*100 #calculate %T from pixel values
    data['OD']= 2-n.log10(data['%T']) #convert %T into OD
    data.to_csv(f'{file}_OD_{date.today()}.csv')
    #return(data)

OD(x,y)


#Author: Nick Howell (nrhowell@gmail.com)