import argparse

def parse_args(): #FIXME
    parser = argparse.ArgumentParser(
        description="This script collects transcript expression data output by Stringtie and calculates"
        "Sex-specific mean FPKM values per scaffold.")
    parser.add_argument(
        '--sex', nargs = '+', help='A space separated list of sexes ("male" or "female"). Order must be the same as --input_files.')
    parser.add_argument(
        '--input_files', nargs='+', help = 'A space-separated list of t_data.ctab input files.')
    args = parser.parse_args()
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
                    t_data[tid]['m'].append(fpkm)
                else:
                    t_data[tid]['f'].append(fpkm)

                                                         
if __name__ == "__main__":
    main()
