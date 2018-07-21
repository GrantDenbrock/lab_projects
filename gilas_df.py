import os
import numpy as np
import pandas as pd
import os

sample_list=[]
rna_samples=[]
parameters=[]
data=[]

#sample_list and rna_samples
files = [f for f in os.listdir('.') if os.path.isfile(f)]
for f in files:
    if f.endswith('.stats')==True:
        sample_list.append(f)
    if '.rna.' in f:
        rna_samples.append(f)
print('printing sample list')
print(sample_list)
#parameters
with open('parameters.txt', 'r') as readfile:
    for line in readfile:
        parameter=line.strip() #may want to strip semicolons and apostrophes in future!
        if parameter != '':
            parameters.append(parameter)
#parameters are to become row/column names

#dataframe
gilas_df = pd.DataFrame(index=sample_list, columns=parameters)
print(gilas_df)

temporary_list=[]
files = [f for f in os.listdir('.') if os.path.isfile(f)]
for f in files:
    for sample in sample_list:
        for parameter in parameters:
            if f.endswith(sample + '.data.txt')==True:
                with open (sample + '.data.txt', 'r') as readfile:
                    print('printing readfile')
                    print(readfile)
                    for line in readfile:
                        gilas_df.loc[sample,parameter]=line
print(gilas_df)
