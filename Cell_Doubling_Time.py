"""
Doubling time calculator
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Calculates the doubling times, or projected growth, of cell cultures for populations experiencing exponential growth.

How to use:
import Cell_doubling_time as dt

dt.DoublingTime(t0, tn, te)
    Returns the doubling time for an exponentially expanding cell populaiton.
    t0 = cells number time =0
    tn = cell number at time =n
    te = time elapsed between t0 and tn in hours
    
dt.CellNumber(t0,tn,te,tr)
    Returns a dataframe containing the projected growth of an exponentially 
    expanding cell population.
    t0 = cells number time =0
    tn = cell number at time =n
    te = time elapsed between t0 and tn in hours
    tr = the projected time of growth of the population, before reaching confluency, in hours
    
dt.CellNUmberDT(t0,DT,tr)
    t0 = cells number at time =0
    DT = doubling time in hours
    tr = the projected time of growth of the population, before reaching confluency, in hours


author: Nick Howell
        nrhowell@gmail.com
"""

import math as m
import pandas as pd

def DoublingTime (t0, tn, te):
    """
    t0 = cells at time 0
    tn = cells at time n
    te = time ellapsed between t0 and tn
    """
    DT = (m.log(2))/((m.log(tn/t0))/te)
    print(f"{DT} hours")
    return DT

def CellNumber (t0, tn, te, tr):
    """
    t0 = cells at time 0
    tn = cells at time n
    te = time ellapsed between t0 and tn
    tr = the projected time for growth, before reaching confluencey
    """
    GR = (m.log(tn/t0))/te  #growth rate calculation
    
    cells = []
    hours = []

    for value in range(tr):
        Nt = t0*m.exp(GR*value)
        hours.append(value)
        cells.append(Nt)
        data = {'Cell Number':cells, 'Hours':hours}
    df = pd.DataFrame(data)
    return df

def CellNumberDT (t0, DT, tr):
    """
    t0 = cells at time 0
    DT = doubling time
    tr = the projected time for growth, before reaching confluencey
    """
    cells = int(t0*2**(tr/DT))
    gens = int(tr/DT)
    print(f"""{gens} generations
{cells} cells""")
    return cells
    