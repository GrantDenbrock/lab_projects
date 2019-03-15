
#!/usr/bin/env python
#https://gist.github.com/slowkow/8101481
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#Borrowing part of this script from Kamil Slowikowski credited below. His script neatly strips data from gff3 format into a dataframe.
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
GTF.py
Kamil Slowikowski
December 24, 2013
Read GFF/GTF files. Works with gzip compressed files and pandas.
    http://useast.ensembl.org/info/website/upload/gff.html
LICENSE
This is free and unencumbered software released into the public domain.
Anyone is free to copy, modify, publish, use, compile, sell, or
distribute this software, either in source code form or as a compiled
binary, for any purpose, commercial or non-commercial, and by any
means.
In jurisdictions that recognize copyright laws, the author or authors
of this software dedicate any and all copyright interest in the
software to the public domain. We make this dedication for the benefit
of the public at large and to the detriment of our heirs and
successors. We intend this dedication to be an overt act of
relinquishment in perpetuity of all present and future rights to this
software under copyright law.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.
For more information, please refer to <http://unlicense.org/>
"""
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from collections import defaultdict
import gzip
import pandas as pd
import re
from collections import Counter
import csv
import argparse
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def parse_args():
	parser = argparse.ArgumentParser(
		description="This script collects transcript expression data output "
		"by Stringtie and calculates"
		"Sex-specific mean FPKM values per scaffold.")

	parser.add_argument(
		"--input_file", nargs="+",
		help="A gff3 file. For Example: 'Gila.gff3' ")

        args = parser.parse_args()
        return args
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

GTF_HEADER  = ['seqname', 'source', 'feature', 'start', 'end', 'score',
               'strand', 'frame']
R_SEMICOLON = re.compile(r'\s*;\s*')
R_COMMA     = re.compile(r'\s*,\s*')
R_KEYVALUE  = re.compile(r'(\s+|\s*=\s*)')

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def dataframe(filename):
    """Open an optionally gzipped GTF file and return a pandas.DataFrame.
    """
    # Each column is a list stored as a value in this dict.
    result = defaultdict(list)

    for i, line in enumerate(lines(filename)): #see lines() below
        for key in line.keys():
            # This key has not been seen yet, so set it to None for all
            # previous lines.
            if key not in result:
                result[key] = [None] * i

        # Ensure this row has some value for each column.
        for key in result.keys():
            result[key].append(line.get(key, None))

    return pd.DataFrame(result)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def lines(filename):
    """Open an optionally gzipped GTF file and generate a dict for each line.
    """
    fn_open = gzip.open if filename.endswith('.gz') else open

    with fn_open(filename) as fh:
        for line in fh:
            if line.startswith('#'):
                continue
            else:
                yield parse(line) #see parse(line) below converts each line to a dict.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def parse(line):
    """Parse a single GTF line and return a dict.
    """
    result = {} #dictionary to hold the line

    fields = line.rstrip().split('\t') #strip the whitespace off right side of each field and separate by tabs

    for i, col in enumerate(GTF_HEADER):
        result[col] = _get_value(fields[i]) #see _get_value() below

    # INFO field consists of "key1=value;key2=value;...".
    infos = [x for x in re.split(R_SEMICOLON, fields[8]) if x.strip()]

    for i, info in enumerate(infos, 1):
        # It should be key="value".
        try:
            key, _, value = re.split(R_KEYVALUE, info, 1)
        # But sometimes it is just "value".
        except ValueError:
            key = 'INFO{}'.format(i)
            value = info
        # Ignore the field if there is no value.
        if value:
            result[key] = _get_value(value)

    return result
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def _get_value(value):
    if not value:
        return None

    # Strip double and single quotes.
    value = value.strip('"\'')

    # Return a list if the value has a comma.
    if ',' in value:
        value = re.split(R_COMMA, value)
    # These values are equivalent to None.
    elif value in ['', '.', 'NA']:
        return None

    return value
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
### this function takes a list of a subset of scaffolds we are interested in and counts the number of genes that are attributed to that scaffold. It returns a dictionary of chrom : count.
def count_genes(chroms_to_inspect, dataframe): #should take a list of chroms to inspect and see how many genes are on each
    chrom_count_dict = Counter(dataframe.seqname) # makes a dictionary of chrom : count of genes
    chroms_to_inspect = set(chroms_to_inspect) #remove the duplicate entries. The dataframe lists each gene product therefore some scaffolds are repeated like 100 times. Remove those duplicates.
    dictionary = {} # this will hold the entries we are interested in
    for chrom in chroms_to_inspect: #in the set of chroms we are interested in
        if str(chrom) in chrom_count_dict: #if the chromosome is in the chrom : count dictionary
            dictionary[chrom] = chrom_count_dict[str(chrom)] #add that to our new dictionary
        return(dictionary) #return that new dictionary
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
### creates a dictionary of chrom : [gene names]
def gene_name_dict(dataframe): # takes the dataframe created above of all the gff data as input
    gene_name_dict = {} # dictionary of chrom : list of gene names
    for x in range(len(dataframe)): # for each entry in the dataframe
        currentid = dataframe.iloc[x,0] # scaffold
        currentvalue = dataframe.iloc[x,9] #FIXME get Name r.t source gene. Fixed, changed 11->9. # gene name
        gene_name_dict.setdefault(currentid, []) # make the entry into the dictionary
        gene_name_dict[currentid].append(currentvalue) # put the gene names into the list
    return(gene_name_dict) # return that dictionary
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
### is this function completely redundant? NO it pulls out just the sex chrom entries. Seems WAAAAAY overcomplicated...
def get_gene_names(chroms_to_inspect, dataframe):
    dict_of_gene_names = gene_name_dict(dataframe) # grabs a gene_name_dict from the function gene_name_dict
    new_dict = {} # this dict will hold sex chrom : list of gene names
    for chrom in chroms_to_inspect: #for each entry in our list of sex chroms
        for chrom in dict_of_gene_names: # for each entry in our list that is in dict of gene names
            new_dict[str(chrom)] = dict_of_gene_names[str(chrom)] #add that entry to new_dict as chrom : [gene names]
        return(new_dict)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def main():
    args = parse_args()
    #making the dataframe and outputting to csv and html
    new_df = dataframe(args.input_file) #makes the dataframe out of our gff input file
    new_df.to_csv('raw_gene_df.csv')
    print('created raw_gene_df.csv')
    gene_df = new_df[new_df.feature == 'gene'] #make new dataframe that contains only the gene features
    gene_df.to_html('gene_stats.html') # put into an html for inspection
    print('created gene_stats.html')
    gene_df.to_csv('gene_stats.csv') # put into a csv in case we want to do something else with it
    print('created gene_stats.csv')
    print("The total number of genes across all scaffolds is: ", len(gene_df.index)) # output the number of genes total in this gff
    #need to count genes across all scaffolds
    #need to get a new chroms to inspect, call it all_chroms
    all_chroms = [chrom for chrom in gene_df.seqname] #all chroms = 00000000....,1111.....,.....222324,222324,222324,222324,.... etc
    all_chroms_uniq = set(all_chroms) # remove duplicate values
    all_chroms_uniq_sorted = sorted(all_chroms_uniq) # a list in numerical order of all the scaffolds

    # ~~~~~~~~~~gene count per scaffold~~~~~~~~~~~~~~
    cnt = Counter()
    for chrom in all_chroms: #for each entry in all chroms (and since each seq name corresponds to one gene)
        cnt[chrom]+=1 # tally it and add it to the counter object
    #write it out to csv
    with open('gene_count_per_scaffold.csv', encoding='utf-8-sig', mode='w') as fp:
        fp.write('chrom,count\n')
        for tag, count in cnt.items():
            fp.write('{},{}\n'.format(tag, count))

    # #need to get the gene names for genes located on putative sex scaffolds
    # putative_sex_chroms = [157,218,304,398,674,220562] # list of putative sex chroms
    # gene_name_dict = get_gene_names(putative_sex_chroms, gene_df) #make a dictionary of gene names per putative sex scaff
    # gene_name_dataframe = pd.DataFrame.from_dict(gene_name_dict, orient='index') #make a dataframe out of that dict
    # gene_name_dataframe.to_csv('gene_name_dataframe.csv')


if __name__ == "__main__":
    main()
