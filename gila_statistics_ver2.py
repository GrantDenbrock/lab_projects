import os
import numpy as np
import pandas as pd
import re
import argparse

#implement args ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def parse_args():
    parser = argparse.ArgumentParser(
        description="This script collects transcript expression data output by Stringtie and calculates"
        "Sex-specific mean FPKM values per scaffold.")

    parser.add_argument(
        '--input_files', nargs = '+', help='Enter a space seperated list of sorted bam input files. For example: "sample1.sample1.dna.mkdup.sorted.bam.stats".')

    parser.add_argument(
        '--output_html_df', help='Enter the name you want to use for the html formatted output dataframe. For example: "gila_stats_dataframe.html". ')

    args = parser.parse_args()

    # for x in args.sex:
    #     if x not in ['male','female']:
    #         raise ValueError('Sex not specified correctly, must be either "male" or "female".')
    #
    # if len(args.sex) != len(args.input_files):
    #     raise ValueError("Input lengths do not match sex lengths")

    return args
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def main():
    args=parse_args()
    filenames = args.input_files

    dataframe = pd.read_csv(filenames[0], sep = ':', comment = '#', header = None)
    #print('printing df1', dataframe)

    for filename in filenames[1:]:
        df = pd.read_csv(filename, sep = ':', comment = '#', header = None)
        dataframe = pd.merge(dataframe, df, how = 'outer', on = 0)

    dataframe.columns = ['samples'] + filenames
    dataframe = dataframe.replace(r'\t','', regex=True)
    dataframe = dataframe.transpose()
    dataframe.columns = dataframe.iloc[0]
    df2 = dataframe.iloc[1:].copy()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #CALCULATIONS
    df2['reads mapped ratio'] = df2['reads mapped'] / df2['raw total sequences']
    df2['percent unmapped'] = df2['reads unmapped']/df2['raw total sequences']
    df2['estimated coverage'] = df2['reads mapped']*df2['average length']/df2['total length']
     #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
     #clean look at the dataframe
    df2.to_html(args.output_html_df)

if __name__ == "__main__":
    main()


#~~~~~~~~~~~~ RUNME ~~~~~~~~~~~~~~~~~~ do they need quotation marks?

#    python gila_statistics_ver2.py --input_files G_10_dna.gila1.dna.mkdup.sorted.bam.stats G_16_dna.gila1.dna.mkdup.sorted.bam.stats G_30_dna.gila1.dna.mkdup.sorted.bam.stats G_35_dna.gila1.dna.mkdup.sorted.bam.stats G_KI01_dna.gila1.dna.mkdup.sorted.bam.stats G_L_dna.gila1.dna.mkdup.sorted.bam.stats --output_html_df gila_statistics_output_df.html
