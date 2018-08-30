import argparse
from statistics import mean

def parse_args():
    parser = argparse.ArgumentParser(
        description="This script collects transcript expression data output by Stringtie and calculates"
        "Sex-specific mean FPKM values per scaffold.")
    parser.add_argument(
        '--sex', nargs = '+', help='A space separated list of sexes ("male" or "female"). Order must be the same as --input_files.')
    parser.add_argument(
        '--input_files', nargs='+', help = 'A space-separated list of t_data.ctab input files.')
    args = parser.parse_args()

    for x in args.sex:
        if x not in ['male','female']:
            raise ValueError('Sex not specified correctly, must be either "male" or "female".')

    if len(args.sex) != len(args.input_files):
        raise ValueError("Input lengths do not match sex lengths")

    return args

def get_transcript_average(transcript,dict,sex): #seperating by sex allows us to automatically filter male and fpkm.
    for transcript in dict:
        if sex == 'm':
            male_list = dict[transcript]['m']
            print(mean(male_list))
        else:
            female_list = dict[transcript]['f']
            print(mean(female_list))

            
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

    print(t_data)
    for ts in range(len(t_data)):
        male_ts = get_transcript_average(ts,t_data, 'm')
        fem_ts = get_transcript_average(ts,t_data, 'f')
        print('The average male FPKM for transcript: '+ ts + ' is ' + male_ts + 'and the average female FPKM for transcript: ' + ts + ' is ' + fem_ts)






if __name__ == "__main__":
    main()
