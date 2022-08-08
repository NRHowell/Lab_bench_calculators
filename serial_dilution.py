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
import serial_dilution as sd
sd.dilution_series(SC,DilF,steps,vol,rep,plate,conc_units,vol_units,priority)


~Stock solution calculator~

Calculates the concentration of stock solutions. Asks for user inputs depnding on the test. Be mindful of inputing values with equivalent units. Contains three tests:
    'volume' - returns the volume required to achieve a required concentration
    'mass' - returns the mass required to achieve the required concentration at a defined volume
    'conc' - return the concentraiton of a solution with a defined mass and volume
        
How to use:
import serial_dilution as sd
sd.stock_solution(test,units)


~Stock dilution calculator~

Calculates the volume of stock solution and dilutent required to achieve the initial concentration of the dilution series
    'stock_concentration' = the concentration fo the stock solution
    'first dilution' = the concentration of the initial solution of the dilution series
    'volume' = the volume of the solution required
    'units' = the units being used
note:ensure units being used are equivalent

How to use:
import serial_dilution as sd
sd.stock_dilution(stock_concentration,first_dilution,volume,units)
"""
from pandas import DataFrame as df
import toml
plate_data = toml.load('plate-data.toml')

def dilution_series(SC,DilF,steps,vol,rep,plate,conc_units,vol_units,priority):
    def data_test():
        """sanity check the basic data"""
        if steps*rep > plate:
            return print(f"Error: Maximum wells available is {plate}. Review the number of steps or reps required")
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


def stock_solution(test,units):
    """
    Simple calculator for calculating the concentration of stock solutions. Contains three tests:
        1. 'volume' - returns the volume required to achieve a required concentration
        2. 'mass' - returns the mass required to achieve the required concentration at a defined volume
        3. 'conc' - return the concentraiton of a solution with a defined mass and volume
    """
    def volume(mass, MW, conc):
        """to return the volume required to achieve a required concentration"""
        vol = (mass/MW)/conc
        return vol

    def mass(MW, vol, conc):
        """to return the mass required to achieve the required concentration at a defined volume"""
        mg = (conc*vol)*MW
        return mg

    def conc(mass, MW, vol):
        """to return the concentraiton of a solution with a defined mass and volume"""
        molarity = (mass/MW)/vol
        return molarity

    if test == 'volume':
        mass = float(input('mass of substance =    '))
        MW = float(input('Molecular weight of the substance =   '))
        conc = float(input('Desired concentration =     '))
        result = volume(mass,MW,conc)
    elif test == 'mass':
        MW = float(input('Molecular weight of the substance =   '))
        vol = float(input('Final volume required =    '))
        conc = float(input('Desired concentration =     '))
        result  = mass(MW,vol,conc)

    elif test == 'molarity':
        mass = float(input('mass of substance =    '))
        MW = float(input('Molecular weight of the substance =   '))
        vol = float(input('Final volume required =    '))
        result = conc(mass,MW,vol)

    else:print("Choose to return the 'volume', 'mass' or 'molarity'")
    print(f"{result}{units}")
    return result

def stock_dilution(stock_concentration, first_dilution, volume, units):
    """
    to calculate the dilution from the stock solution to achieve the desired starting concentration of the dilution series
    'stock_concentration' = the concentration fo the stock solution
    'first dilution' = the concentration of the initial solution of the dilution series
    'volume' = the volume of the solution required
    'units' = the units being used
    note:ensure units being used are equivalent
    """
    
    vol_stock = (first_dilution/stock_concentration)*volume
    vol_diluent = volume - vol_stock
    print (f"{vol_stock}{units} of stock solution + {vol_diluent}{units} of dilutent")
    return vol_stock
    

"""
Author:
Nicholas Howell
nrhowell@gmail.com
"""
