import argparse
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt


#~~~~~~~~ Let's get some args going ~~~~~~~~~~~~~~~~~~~
def parse_args():
    parser = argparse.ArgumentParser(
        description="This script takes a csv from gila_expression and plots the count of f_m_ratio of fpkm.")

    parser.add_argument(
        '--input_file', nargs='+', dest='input_file',  help = 'Enter the name of csv to make a plot from.')

    parser.add_argument(
        '--num_bins', required=True, default = 1000,
        help="Enter the desired number of bins for your histogram.")

    parser.add_argument(
        '--range', default = 4,
        help = "Enter the desired upper limit for the range of your histogram.")

    parser.add_argument(
        '--color', default = 'orange',
        help="Enter the color of the bars of your histogram.")

    parser.add_argument(
        '--output_file', required=True,
        help="Name of and full path to output histogram plot. Will overwrite if already exists.")

    args = parser.parse_args()

    return args
#~~~~~~~~~~ and for the script ~~~~~~~~~~~~~~~~~~~~~~
def main():

    args = parse_args()

    inputfile = args.input_file[0]
    print(inputfile)
    num_bins = args.num_bins
    print(num_bins)


    df = pd.read_csv(inputfile, sep = '\t') #reads our input file into a df
    df_no_inf = df[~df.isin([np.nan, np.inf, -np.inf]).any(1)] #gets rid of nans and infs
    df_list=df_no_inf['f_m_ratio'].tolist() #throws it into a list for plotting

    df_nan = df.loc[pd.isnull(df.f_m_ratio)] #makes a dataframe of all the nan values. For later reference
    df_nan.to_html('nan_gila.html')

    df_inf = df[df.isin([np.nan, np.inf, -np.inf]).any(1)] #makes a dataframe of the inf values For later reference
    df_inf.to_html('inf_gila.html')


    fig, ax = plt.subplots()

    # the histogram of the data
    n, bins, patches = ax.hist(df_list, int(num_bins), color = args.color, range = (0,args.range))

    ax.set_xlabel('Female/Male FPKM Ratio')
    ax.set_ylabel('Count')
    ax.set_title(r'Count of Female to Male Ratio')

    # Tweak spacing to prevent clipping of ylabel
    fig.tight_layout()
    plt.show()
    fig.savefig(args.output_file)

if __name__ == "__main__":
    main()
