import argparse
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from string import ascii_uppercase


#FIXME implement args ~~~~~~~~~~~~~~~~~~~~~~~~~~
def parse_args():
    parser = argparse.ArgumentParser(
        description="This script collects transcript expression data output by Stringtie and calculates"
        "Sex-specific mean FPKM values per scaffold.")

    parser.add_argument(
        '--input_files', nargs = '+', help='Enter the output from gila_chromstats.py followed by the output from gila_expression.py seperated by a space. ')

    parser.add_argument(
        '--output_html_df', help='Enter the name you want to use for the html formatted output dataframe. For example: "gila_big_dataframe.html". ')

    args = parser.parse_args()

    # for x in args.sex:
    #     if x not in ['male','female']:
    #         raise ValueError('Sex not specified correctly, must be either "male" or "female".')
    #
    # if len(args.sex) != len(args.input_files):
    #     raise ValueError("Input lengths do not match sex lengths")

    return args

#~~~~~~~~~~~~~ gifted from stackexchange ~~~~~~~~~~~~~~~~~
def shifter(df, col_to_shift, pos_to_move):
    arr = df.columns.values
    idx = df.columns.get_loc(col_to_shift)
    if idx == pos_to_move:
        pass
    elif idx > pos_to_move:
        arr[pos_to_move+1: idx+1] = arr[pos_to_move: idx]
    else:
        arr[idx: pos_to_move] = arr[idx+1: pos_to_move+1]
    arr[pos_to_move] = col_to_shift
    df.columns = arr
    return df
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def main():
    args=parse_args()
    input_1 = args.input_files[0] #Chromstats file
    input_2 = args.input_files[1] #FPKM data Want to keep the nargs here because it needs multiple files and only the first 2.

    df_1 = pd.read_csv(input_1, sep = '\t')
    #df_1.to_html('df_1.html')
    df_2 = pd.read_csv(input_2, sep = '\t')
    #df_2.to_html('df_2.html')

    big_df = pd.merge(df_1,df_2, left_on='chrom', right_on='scaffold')
    big_df = big_df.drop({'scaffold','G_10_dna.gila1.mkdup.sorted.bam','G_16_dna.gila1.mkdup.sorted.bam', 'G_30_dna.gila1.mkdup.sorted.bam', 'G_35_dna.gila1.mkdup.sorted.bam', 'G_KI01_dna.gila1.mkdup.sorted.bam', 'G_L_dna.gila1.mkdup.sorted.bam'}, axis = 1)
    big_df = big_df.rename(columns = {'chrom':'scaffold', 'male_sum':'male_sum_exp', 'female_sum':'female_sum_exp'})

    big_df = big_df.pipe(shifter, 'length', 1) #works like a charm


    big_df.to_html(args.output_html_df)

    #big_df = big_df[['','','']] #what in the world is this?

if __name__ == "__main__":
    main()
#~~~~~~~~~~~~~ RUNME ~~~~~~~~~~~~~~~~~~

#     python gila_big_dataframe.py --input_files 'gila_chromstats_df.txt' 'gila_expression_1.txt' --output_html_df gila_big_dataframe_html_df.html
