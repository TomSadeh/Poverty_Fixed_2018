import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def nefesh_btl(nefesh):
    """
    Parameters
    ----------
    nefesh : int
        The number of persons the household has.

    Returns
    -------
    Float
        The standardised number of persons in the household, 
        according to National Security Institue and the Central Bureau of Statistics definition.
    
    Required libraries
    ------------------
    None.

    """
    l = [1.25, 2, 2.65, 3.2, 3.75, 4.25, 4.75, 5.2]
    if nefesh <= len(l) - 1:
        return l[int(nefesh - 1)]
    else:
        return 5.6 + (nefesh - 9) * 0.4

def invert(string):
    """
    A function which invert a string.
    Parameters
    ----------
    string : string
        the string to invert.

    Returns
    -------
    string
        An inverted string.

    Required libraries
    ------------------
    None.
    """
    return string[::-1]
   
# Complete the address here, and change the names in the file itself for your own folders and file names.
file_names = pd.read_csv(r'File Names.csv') 

# Enter the address of the base folder here.
base_address = r'' 

# Complete the address here.
cpi = pd.read_csv(r'CPI.csv', index_col = 'Year') 

# Making 2018 the base year.
cpi['base 2018'] = cpi['CPI'] / cpi.loc[2018,'CPI'] * 100 

# The 2018 poverty threshold according to the National Insurance Institute.
poverty_threshold = 2875 

# Creating an empty DataFrame to contain the results.
results = pd.DataFrame()

# The main loop of the calculations.
for year, folder, file in zip(file_names['Year'], file_names['Folder Address'], file_names['File Name MB']):
    
    # Reading a survey file.
    df = pd.read_csv(base_address + '\\' + folder + '\\' + file + '.csv')
    
    # Calculating standard persons for years that the file doesn't contain them.
    if 'nefeshstandartit' not in df.columns:
        df['nefeshstandartit'] = df['nefashot'].apply(nefesh_btl)
        
    # Renaming the mishkal column to a uniform name.
    if 'mishkal' in df.columns:
        df.rename(columns = {'mishkal' : 'weight'}, inplace = True)
        
    # Calculating the poverty ratio, by slicing the DataFrame to only households below the threshold, after dividing the income per standard person by the cpi, and dividng the whole affair by the total number of households to get the ratio.
    results.loc[year, 'Poverty'] = df[(df['net']/df['nefeshstandartit'] / cpi.loc[year, 'base 2018'] * 100) <= poverty_threshold]['weight'].sum() / df['weight'].sum()

# Creating the figure.
plt.figure(figsize = (10,5))  
plt.rc('font', family = 'David')  
plt.plot(results.index, results['Poverty'], label = invert('שיעורי עוני לפי קו 8102'), marker = 'o', markersize = 4)
plt.xlabel(invert('שנה'), fontsize = 15)
plt.ylabel(invert('שיעור עוני מקובע ל-8102'), fontsize = 15)
plt.title(invert('שיעורי עוני מקובעים בשנים 8102-5002'), fontsize = 20)
plt.xticks(np.arange(2005, 2019), fontsize = 12)
labels = list(map(str, np.arange(0, 45, step = 5)))
for i in range(len(labels)):
    labels[i] += '%'
plt.yticks(np.arange(0, 0.425, step = 0.05), labels = labels, fontsize = 12)
plt.axvline(2011.5, label = invert('שינוי מתודולוגי'), color = 'black', linestyle = '--', alpha = 0.7)
for i in results.index:
    plt.annotate(str(round(results.loc[i,'Poverty'] * 100, 1)) + '%', (i-0.35,results.loc[i,'Poverty'] + 0.015))
plt.legend()

# Insert the address to save the figure here.
figure_address = r''
plt.savefig(figure_address + '\\' + 'Poverty fixed 2005-2018.png') 