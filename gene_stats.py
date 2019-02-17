
#!/usr/bin/env python
#https://gist.github.com/slowkow/8101481
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#Borrowing part of this script from Kamil Slowikowski credited below. His script neatly strips data from gff3 format into a dataframe.
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
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


GTF_HEADER  = ['seqname', 'source', 'feature', 'start', 'end', 'score',
               'strand', 'frame']
R_SEMICOLON = re.compile(r'\s*;\s*')
R_COMMA     = re.compile(r'\s*,\s*')
R_KEYVALUE  = re.compile(r'(\s+|\s*=\s*)')


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

def count_genes(chroms_to_inspect, dataframe):
    chrom_count_dict = Counter(dataframe.seqname)
    for chrom in chroms_to_inspect:
        if str(chrom) in chrom_count_dict:
            print(chrom, " : ", chrom_count_dict[str(chrom)]) #FIXME I dont want this to always print. Just for prototyping

#going to put the genes per scaffold into a dictionary because dicts and dataframes play nicely together
def gene_name_dict(dataframe):
    gene_name_dict = {}
    for x in range(len(dataframe)):
        currentid = dataframe.iloc[x,0]
        currentvalue = dataframe.iloc[x,11]
        gene_name_dict.setdefault(currentid, [])
        gene_name_dict[currentid].append(currentvalue)
    return(gene_name_dict)



def main():
    new_df = dataframe('Gila.gff3') #makes the dataframe out of our gff file
    gene_df = new_df[new_df.feature == 'gene'] #make new dataframe that contains only the gene features
    gene_df.to_html('gene_stats.html') # put into an html for inspection
    gene_df.to_csv('gene_stats.csv') # put into a csv in case we want to do something else with it
    print("The number of genes is: ", len(gene_df.index)) # output the number of genes total in this gff
    print('~~~~~~~~~~~~~~Output of gene count~~~~~~~~~~~~~~~~~~~')
    putative_sex_chroms = [157,218,304,398,674,220562] # list of putative sex chroms
    count_genes(putative_sex_chroms,gene_df) # will output the number of genes attributed to each putative sex chrom
    print(gene_name_dict(gene_df))

if __name__ == "__main__":
    main()
