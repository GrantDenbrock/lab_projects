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

list_of_dfs = [pd.read_csv(filename, sep = ':') for filename in filenames]
for dataframe, filename in zip(list_of_dfs, filenames):
  dataframe['filename'] = filename

combined_df = pd.concat(list_of_dfs, ignore_index=True, axis=1)
#if datatype of df column != int remove it except if it is column 1
#then fix the column names

print(combined_df)
