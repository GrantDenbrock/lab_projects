import pandas as pd
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

inputfile = "~/lab_projects/test.txt" #FIXME implement args for this

df = pd.read_csv(inputfile, sep = '\t')
df.to_html('plot_gila_df.html')
df_list=df['f_m_ratio'].tolist()
#print(df_list) #has a bunch of "inf"'s and "nan"'s !!
new_df_list = [x for x in df_list if float(x) != 'nan'] #FIXME I cant get rid of the nans and infs!
new_df_list = [x for x in df_list if float(x) != 'inf']
new_df_list = [x for x in df_list if str(x) != 'nan']
new_df_list = [x for x in df_list if str(x) != 'inf']
new_df_list = [x for x in df_list if ~np.isnan(x)]
new_df_list = [x for x in df_list if ~np.isinf(x)]
new_df_list = [x for x in df_list if type(x) == float] # => they are all floats.
#print(new_df_list)
#I know that the nans and infs are floats.
#I know they are there in my list because I print the list and see it with my eyes.
try:
    df_list.remove('nan') #but this says nan not in list!
except:
    pass

try:
    df_list.remove(nan) #and this says nan not defined. Clearly I dont understand something here.
except:
    pass
try:
    df_list.remove(inf)
except:
    pass
df_list = list(filter(lambda x: x!= 'nan', df_list)) #nope
print(df_list)

#I would make a plot, but I havent got a working list out of the df yet.
num_bins = 10

fig, ax = plt.subplots()

# the histogram of the data
n, bins, patches = ax.hist(new_df_list, num_bins = 10, color='orange')

ax.set_xlabel('FPKM')
ax.set_ylabel('Frequency')
ax.set_title(r'FPKM Frequency of different')

# Tweak spacing to prevent clipping of ylabel
fig.tight_layout()
plt.show()
