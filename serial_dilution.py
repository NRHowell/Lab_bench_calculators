"""
~Serial Dilution Calculator~

Calculates a dilution series from a starting concentration, dilution factor and required volume.
The dilution series will be formatted into a standard assay plate format (e.g. 96,48, 384 etc. etc.)

SC = starting concentration
DilF = dilution factor
steps = the number of steps required to reach final dilution
vol = required volume (take into account volume required for the dilution itself)
rep = the number of replicates for each dilution
plate = the number of wells in the plate, or the number of wells available to use
conc_units = the units of concentration (e.g. 'mM','ug/ml')
vol_units = the units of volume (e.g. 'ul', 'ml')
priority = 'row' or 'collumn

How to use:
Script calls on addition data located in 'plate_data.toml'

import serial_dilution as sd
sd.dilution_series(SC,DilF,steps,vol,rep,plate,conc_units,vol_units,priority)

"""
from pandas import DataFrame as df
import toml
plate_data = toml.load('plate-data.toml')

def dilution_series(SC,DilF,steps,vol,rep,plate,conc_units,vol_units,priority):
    def data_test():
        """sanity check the basic data"""
        if steps*rep > plate:
            return print("Error: Maximum wells available is ",plate,". Review the number of steps or reps required")
    def d_s():
        """The actual dilution series"""
        n = SC
        conc_list=[SC]
        for dil in conc_list:
            dil = n/DilF
            n = dil
            conc_list.append(dil)

            if len(conc_list) == steps:
                break
        return conc_list
    def volumes():
        """Calculates the volume of the compound required from the stock solution or the previous dilution"""
        x = vol
        vol_list = [x/DilF]
        for volume in vol_list:
            volume = x/DilF
            vol_list.append(volume)
            if len(vol_list) == steps:
                break
        return vol_list
    def final_volumes():
        """Calculates the volume of diluent required to achieve the desired concentration"""
        y = vol
        fvol_list = [vol-(y/DilF)]
        for fvol in fvol_list:
            fvol = y-y/DilF
            fvol_list.append(fvol)
            if len(fvol_list) == steps:
                break
        return fvol_list
    def collumn_priority():
        """Formats the dilution series based on collumn priority i.e A1,B1,C1..."""
        val = []
        row = plate_data['plate'][str(plate)]
        collumn = 1
        x = 0
        r = row[x]
        for location in range(steps):
            r = row[x]
            x = x+1
            location = (r, collumn)
            if x == len(row):
                x = 0
                collumn = collumn+rep
            val.append(location)
            #if plate_data['plate']['num'][str(plate)] >= collumn+1:
                #return "error: available wells exceeded"
        return val
    def row_priority():
        """Formats the dilution series based on row priority i.e A1,A2,A3..."""
        val = []
        row = plate_data['plate'][str(plate)]
        collumn = 1
        x = 0
        for location in range(steps):
            r = row[x]
            location = (r, collumn)
            collumn = collumn + rep
            if collumn > plate_data['plate']['num'][str(plate)]:
                x = x+1
                collumn = 1
            val.append(location)
            if collumn >= plate_data['plate']['num'][str(plate)]:
                return "error: available wells exceeded"
        return val
    def data_output():
        """
        Assemble the dilution series!!!
        """
        data_test()
        if priority == 'collumn':
            loc = collumn_priority()
        elif priority == 'row':
            loc = row_priority()
        else:
            return print('error, choose "row or "collumn" priority')

        dictionaries = {'Sample':range(1,(steps+1)),'Location':loc, 'Dilution series':d_s(), conc_units:conc_units, 'Compound volume':volumes(), 'Diluent volume':final_volumes(), vol_units:vol_units }
        serial_dilution = df(dictionaries)
        return serial_dilution
    return data_output()
#
# Author:
# Nicholas Howell
# nrhowell@gmail.com
#
