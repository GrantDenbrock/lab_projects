import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt


inputfile = "~/lab_projects/test.txt" #FIXME implement args for this

df = pd.read_csv(inputfile, sep = '\t') #reads our input file into a df
df_no_inf = df[~df.isin([np.nan, np.inf, -np.inf]).any(1)] #gets rid of nans and infs
df_list=df_no_inf['f_m_ratio'].tolist() #throws it into a list for plotting

df_nan = df.loc[pd.isnull(df.f_m_ratio)] #makes a dataframe of all the nan values. For later reference
df_nan.to_html('nan_gila.html')

df_inf = df[df.isin([np.nan, np.inf, -np.inf]).any(1)] #makes a dataframe of the inf values For later reference
df_inf.to_html('inf_gila.html')

num_bins = 1000 #FIXME implement args

fig, ax = plt.subplots()

# the histogram of the data
n, bins, patches = ax.hist(df_list, num_bins, color='orange', range = (0,3)) #FIXME implement args

ax.set_xlabel('Female/Male FPKM Ratio')
ax.set_ylabel('Count')
ax.set_title(r'Count of Female to Male Ratio')

# Tweak spacing to prevent clipping of ylabel
fig.tight_layout()
plt.show()
fig.savefig('histogram_f_m_fpkm_count_0_3.png')

#now make a second histogram of a different window
n, bins, patches = ax.hist(df_list, num_bins, color='orange', range = (0,5)) #FIXME implement args

ax.set_xlabel('Female/Male FPKM Ratio')
ax.set_ylabel('Count')
ax.set_title(r'Count of Female to Male Ratio')

# Tweak spacing to prevent clipping of ylabel
fig.tight_layout()
plt.show()
fig.savefig('histogram_f_m_fpkm_count_0_5.png')
