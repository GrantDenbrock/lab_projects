import os
import numpy as np
import pandas as pd

#import glob package??? to get filenames...
filenames = [
'G_10_dna.gila1.dna.mkdup.sorted.bam.stats',
'G_16_dna.gila1.dna.mkdup.sorted.bam.stats',
'G_30_dna.gila1.dna.mkdup.sorted.bam.stats',
'G_35_dna.gila1.dna.mkdup.sorted.bam.stats',
'G_KI01_dna.gila1.dna.mkdup.sorted.bam.stats',
'G_L_dna.gila1.dna.mkdup.sorted.bam.stats'
]

dataframe = pd.read_csv(filenames[0], sep = ':')

for filename in filenames:
    df = pd.read_csv(filename, sep = ':')
    print('printing df', df)
    dataframe = pd.merge(dataframe, df, how = 'outer', on = 'raw total sequences')

print('printing new dataframe')
print(dataframe)





# list_of_dfs = [pd.read_csv(filename, sep = ':', ) for filename in filenames]
# for filename in filenames:
#     clean_df = pd.merge(clean_df, list_of_dfs[filename], how = "right" , on = "x1")
# print(clean_df)
