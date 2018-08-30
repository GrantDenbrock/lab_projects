import argparse
import numpy as np
import pandas as pd

def parse_args():
    parser = argparse.ArgumentParser(
        description="This script collects transcript expression data output by Stringtie and calculates"
        "Sex-specific mean FPKM values per scaffold.")

    parser.add_argument(
        '--sex', nargs = '+', help='A space separated list of sexes ("male" or "female"). Order must be the same as --input_files.')

    parser.add_argument(
        '--input_files', nargs='+', help = 'A space-separated list of t_data.ctab input files.')

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

            
def main():
    t_ids = {}
    t_data = {}

    args = parse_args()
    for idx, file in enumerate(args.input_files):
        with open(file, 'r') as readfile:
            h = readfile.readline()
            for line in readfile:
                temp_line = line.strip()
                temp_split = temp_line.split()

                tid = temp_split[0]
                chr = temp_split[1]
                fpkm = temp_split[-1]

                if tid not in t_ids:
                    t_ids[tid] = chr

                if tid not in t_data:
                    t_data[tid] = {'m': [], 'f': []}
                if args.sex[idx] == 'male':
                    t_data[tid]['m'].append(float(fpkm))
                else:
                    t_data[tid]['f'].append(float(fpkm))
                    
    mean_table = {}
    for ts in t_data:
        mean_table[ts] = {'m': np.mean(t_data[ts]['m']), 'f': np.mean(t_data[ts]['f'])}
        
    out_dict = {}
    for ts in t_ids:
        scaff = t_ids[ts]
        if scaff is in out_dict:
            out_dict[scaff]['count'] += 1
            out_dict[scaff]['m_sum'] += mean_table['m'][ts]
            out_dict[scaff]['f_sum'] += mean_table['f'][ts]
        else:
            out_dict[scaff] = {'count': 0, 'm_sum': 0, 'f_sum': 0}
            out_dict[scaff]['count'] += 1
            out_dict[scaff]['m_sum'] += mean_table['m'][ts]
            out_dict[scaff]['f_sum'] += mean_table['f'][ts]
    
    table_df = pd.DataFrame.from_dict(out_dict, orient='index').reset_index()
    table_df = table_df.rename(index=str, columns={'index': 'scaffold', 'm_sum': 'male_sum', 'f_sum': 'female_sum'})
    table_df['male_mean'] = table_df.male_sum / table_df.count
    table_df['female_mean'] = table_df.female_sum / table_df.count
    table_df['f_m_ratio'] = table_df.female_mean / table_df.male_mean
    
    table_df.to_csv(args.output_file, sep='\t')


if __name__ == "__main__":
    main()
