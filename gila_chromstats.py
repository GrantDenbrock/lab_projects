import argparse
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def parse_args():
    parser = argparse.ArgumentParser(
        description="This script takes an input file generated from chromstats, and creates a dataframe and plots.")

    parser.add_argument(
        '--sex', nargs = '+', help='A space separated list of sexes ("male" or "female"). Order must be the same as --input_files.')

    parser.add_argument(
        '--input_files', nargs='+', help = 'A space-separated list of t_data.ctab input files.')

    parser.add_argument(
        '--fai', required=True,
        help="Name of and full path to fai file.")

    parser.add_argument(
        '--output_file', required=True,
        help="Name of and full path to output tab-delimited file. Will overwrite if already exists.")

    args = parser.parse_args()

    for x in args.sex:
        if x not in ['male','female']:
            raise ValueError('Sex not specified correctly, must be either "male" or "female".')

    if len(args.sex) != len(args.input_files):
        raise ValueError("Input lengths do not match sex lengths")

    return args
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

inputfile = "~/lab_projects/gila1_chrom_stats_count.txt"
print(inputfile)

df = pd.read_csv(inputfile, sep = '\t')

male_list = ['G_10_dna.gila1.mkdup.sorted.bam', 'G_16_dna.gila1.mkdup.sorted.bam', 'G_KI01_dna.gila1.mkdup.sorted.bam']
female_list = ['G_30_dna.gila1.mkdup.sorted.bam', 'G_35_dna.gila1.mkdup.sorted.bam','G_L_dna.gila1.mkdup.sorted.bam']

df['male_average_cov'] = df[male_list].mean(axis=1)
df['female_average_cov'] = df[female_list].mean(axis=1)
df['f_m_ratio_cov'] = df.female_average_cov/df.male_average_cov
df.to_csv('gila_chromstats_df.txt', sep = '\t', index = False)
df_no_nan = df[~df.isin([np.nan, np.inf, -np.inf]).any(1)] #get rid of nans
#make a df of values that have f_m_ratio less than .95

df.to_html('gila_chromstats_df.html')
df_no_nan.to_html('gila_chromstats_df_no_nan.html')

#if the f_m_ratio is less than .95 add it to another dataframe
df_ratio_less_than = df_no_nan[df_no_nan.f_m_ratio_cov < .95]
df_ratio_less_than.to_html('df_ratio_less_than.html')

#~~~~~~~~~~ plots below ~~~~~~~~~~~~~~
df_no_nan.plot(kind='scatter', x='chrom', y='f_m_ratio_cov', color='orange')
plt.title("Female to Male Ratio across scaffolds")
plt.xlabel("Scaffold Number")
plt.ylabel("Female to Male Ratio")
plt.savefig('gila_chromstats_f_m_ratio.png')
