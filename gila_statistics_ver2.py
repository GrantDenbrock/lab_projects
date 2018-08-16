import os
import numpy as np
import pandas as pd
import re

#import glob package??? to get filenames...
filenames = [
'G_10_dna.gila1.dna.mkdup.sorted.bam.stats',
'G_16_dna.gila1.dna.mkdup.sorted.bam.stats',
'G_30_dna.gila1.dna.mkdup.sorted.bam.stats',
'G_35_dna.gila1.dna.mkdup.sorted.bam.stats',
'G_KI01_dna.gila1.dna.mkdup.sorted.bam.stats',
'G_L_dna.gila1.dna.mkdup.sorted.bam.stats'
]

dataframe = pd.read_csv(filenames[0], sep = ':', header = None)
print('printing df1', dataframe)

for filename in filenames[1:]:
    df = pd.read_csv(filename, sep = ':', comment = '#', header = None)
    dataframe = pd.merge(dataframe, df, how = 'outer', on = 0) #on = 0?

dataframe.columns = ['samples'] + filenames
dataframe = dataframe.replace(r'\t','', regex=True)
dataframe = dataframe.transpose()
dataframe.columns = dataframe.iloc[0]
df2 = dataframe.iloc[1:]

print('printing new dataframe')
print(df2)
