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
    for idx, file in enumerated(args.input_files):
        with open(file, 'r') as readfile:
            h = readfile.readline()
            for line in readfile:
                temp_line = line.strip()
                temp_split = temp_line.split()
                if temp_split[0]
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
                    
                    
    
#     #make room for a class called transcripts
#     class Transcripts:
#         """each transcript will get its own instantiation, and will hold all of the associated values."""
#         def __init__(self): #do I want to include gender, and other values here or just self?

#     for file in input_files:
#         with open(file,'r') as readfile:
#             for line in readfile:
#                 if line == 1:
#                     pass #because the first line is just the headers...
#                 else:
#                     if line.strip(' ')[1] not in transcript_list: # "if the content of the first line is not present in transcript list"
#                         transcript_list.append(line.strip(' ')[1]) #add it to the checklist if it already isnt there
#                         line.strip(' ')[1] = Transcripts() #instantiate the class. Will need to throw in some error handling too. FIXME
#                         line.strip(' ')[1].tid = line.strip('  ')[1]
#                         line.strip(' ')[1].chr = line.strip('  ')[2]
#                         line.strip(' ')[1].strand = line.strip('  ')[3]
#                         line.strip(' ')[1].start = line.strip('  ')[4]
#                         line.strip(' ')[1].end = line.strip('  ')[5]
#                         line.strip(' ')[1].t_name = line.strip('  ')[6]
#                         line.strip(' ')[1].num_exons = line.strip('  ')[7]
#                         line.strip(' ')[1].length = line.strip('  ')[8]
#                         line.strip(' ')[1].gene_id = line.strip('  ')[9]
#                         line.strip(' ')[1].gene_name = line.strip('  ')[10]
#                         line.strip(' ')[1].cov = line.strip('  ')[11]
#                         line.strip(' ')[1].fpkm =  line.strip('  ')[12]
#                     else:
#                         #the class is already instantiated so just add to it...
#                         line.strip(' ')[1].chr.append(line.strip('  ')[2])
#                         line.strip(' ')[1].strand.append(line.strip('  ')[3])
#                         line.strip(' ')[1].start.append(line.strip('  ')[4])
#                         line.strip(' ')[1].end.append(line.strip('  ')[5])
#                         line.strip(' ')[1].t_name.append(line.strip('  ')[6]
#                         line.strip(' ')[1].num_exons.append(line.strip('  ')[7])
#                         line.strip(' ')[1].length.append(line.strip('  ')[8])
#                         line.strip(' ')[1].gene_id.append(line.strip('  ')[9])
#                         line.strip(' ')[1].gene_name.append(line.strip('  ')[10])
#                         line.strip(' ')[1].cov.append(line.strip('  ')[11])
#                         line.strip(' ')[1].fpkm.append(line.strip('  ')[12])
                                                         
if __name__ == "__main__":
    main()
