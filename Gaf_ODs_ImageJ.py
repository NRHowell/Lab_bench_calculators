#!/usr/bin/python

"""For caluclating optical density (OD), or absorbance, from Gafchromic film scanned with the Epson scanner and processed with imageJ. 
Two methods are given, one (OD) takes a series of ROI values, in csv format, and returns the corresponding OD's. The other (optical_density) takes an image file and transforms the image to return a image file calibrated to optical density

OD is calculated using the relationship 'OD = 2-log(%T)'"""


import pandas as pd
import numpy as n
import imageio
from datetime import date

def OD(file,max_trans):
     
    data = pd.read_csv(file)
    data['%T'] = (data['Mean']/max_trans)*100 #calculate %T from pixel values
    data['OD']= 2-n.log10(data['%T']) #convert %T into OD
    data.to_csv(f'{file}_OD_{date.today()}.csv')
    #return(data)  #unhash this and # the above line if you would like the data 'returned' rather than 'saved'


def optical_density(input_path, output_path, maximum_transmission):
    import imageio
    import numpy as np

    tiff_array = imageio.imread(input_path) #read the image file
    trans_array = (tiff_array/maximum_transmission)*100 #calculate % trasmission
    OD_array = 2-np.log10(trans_array)  #calculate the optical densities
    imageio.imwrite(output_path, OD_array) #write the array to a new image file
    print("TIFF image file saved to", output_path)



#Author: Nick Howell (nrhowell@gmail.com)
