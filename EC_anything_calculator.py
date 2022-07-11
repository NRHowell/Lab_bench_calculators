"""
~EC anything calculator~
Returns a range of EC values over a range (0-100) from a given EC50 and Hill slope

"""
import pandas as pd

def EC_anything(start, end, hill, EC50, path):

    global df
    list_ecf = []  # create empty lists to sort outputs
    list_fr = []

    for values in range(start, end, 1):  # determine the range of values and calculate EC value for each one
        EC_values = (((values / (100 - values)) ** (1 / hill)) * EC50)  # calculate the value for the ECF

        list_ecf.append(EC_values)  # store the EC value in this list
        list_fr.append(values)  # store the corresponding range value in this list

        data = {'EC%': list_fr, 'EC value': list_ecf}  # pass lists into dictionary
        df = pd.DataFrame(data)  # pass dictionary into dataframe
    df.to_csv(path)  # output dataframe to csv file
    return df

# author: Nicholas Howell
# nrhowell@gmail.com


#%%
