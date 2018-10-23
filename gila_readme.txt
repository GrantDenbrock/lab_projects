README
~~~~~~~~~~~~~~~~~~~~~~~~
Background

This program is written to analyze the genome of the Gila Monster. The goals are to assemble the genome and describe coverage, dosage compensation, and differential expression between sexes. To do this we must identify putative sex chromosome scaffolds. In order to accomplish this we assembled the reference genomes, and performed quality control and trimming. We chunked these reference genomes into bite sized pieces and used BWA to map the DNA reads to the reference and processed these BAM files. These are the files that will be fed into gila_chromstats.py.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~gila_chromstats.py~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
This script takes a list of input bam files, organizes data from these files into dataframes, and plots the female to male ratio of coverage across scaffolds.

This program requires an input file of count per scaffold per sample. This file comes out of the "rule chromstats dna:". The user can indicate the full path to the file using the flag: --input_file.

--input_file ~/lab_projects/gila1_chrom_stats_count.txt

Along with this input file, it requires the user to input the bam files from males and females seperately. The user can add samples using --male_list and --female_list to indicate the samples sex.

--male_list 'G_10_dna.gila1.mkdup.sorted.bam' 'G_16_dna.gila1.mkdup.sorted.bam' 'G_KI01_dna.gila1.mkdup.sorted.bam' --female_list 'G_30_dna.gila1.mkdup.sorted.bam' 'G_35_dna.gila1.mkdup.sorted.bam' 'G_L_dna.gila1.mkdup.sorted.bam'

 A dataframe containing information from these files will be created; The user should indicate the name of this output file using the flag --output_dataframe. The output will be csv formatted so a .txt extension is recommended.

 --output_dataframe 'gila_chromstats_df.txt'

 That dataframe is also output as html so the user can name that file using the flag: --output_html.

 --output_html 'gila_chromstats_df.html'

Our data came back with NaN and inf values as well that we wished to be able to remove. A seperate dataframe was collected for these values and is output to html. The user can specify the name of this dataframe using the flag: --output_html_no_nan.

--output_html_no_nan 'gila_chromstats_df_no_nan.html'

Scaffolds that did not meet a certain coverage cutoff value were stripped into their own dataframe. The user should specify this cutoff value using the flag: --coverage_cutoff

--coverage_cutoff '.95'

as well as the name of this dataframe using flag: --output_html_cutoff_df .

--output_html_cutoff_df 'df_ratio_less_than.html'

A plot is also created of the female to male ratio per scaffold. The user should specify the filename to hold the plot using the flag: --plot_title.

--plot_title 'gila_chromstats_f_m_ratio.png'

An example run of this program is given below.

python gila_chromstats.py --input_file ~/lab_projects/gila1_chrom_stats_count.txt --male_list 'G_10_dna.gila1.mkdup.sorted.bam' 'G_16_dna.gila1.mkdup.sorted.bam' 'G_KI01_dna.gila1.mkdup.sorted.bam' --female_list 'G_30_dna.gila1.mkdup.sorted.bam' 'G_35_dna.gila1.mkdup.sorted.bam' 'G_L_dna.gila1.mkdup.sorted.bam' --output_dataframe 'gila_chromstats_df.txt' --output_html 'gila_chromstats_df.html'  --output_html_no_nan 'gila_chromstats_df_no_nan.html' --coverage_cutoff '.95' --output_html_cutoff_df 'df_ratio_less_than.html' --plot_title 'gila_chromstats_f_m_ratio.png'
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We then used XYalign's CHROM_STATS on these bam files, yielding our '.stats' files. These .stats files are fed as input into gila_statistics_ver2.py.

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~gila_statistics_ver2.py~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This script is used to calculate the reads mapped ratio, The percent of reads that are unmapped, and the estimated coverage. It takes a list of stats files as input. The user can specify the path to these input files using the flag: --input_files

--input_files  G_10_dna.gila1.dna.mkdup.sorted.bam.stats G_16_dna.gila1.dna.mkdup.sorted.bam.stats G_30_dna.gila1.dna.mkdup.sorted.bam.stats G_35_dna.gila1.dna.mkdup.sorted.bam.stats G_KI01_dna.gila1.dna.mkdup.sorted.bam.stats G_L_dna.gila1.dna.mkdup.sorted.bam.stats

The script then casts this data into a dataframe and 
