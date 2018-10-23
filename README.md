# lab_projects
README
~~~~~~~~~~~~~~~~~~~~~~~~
Background

This series of scripts is written to organize and perform calculations on DNA and RNA mapped reads. The scripts were written to identify putative sex chromosomes for the Gila Monster (Heloderma Suspectum), and provide the means to evaluate expression levels and dosage compensation. The goals of this script are to quantitatively and qualitatively describe coverage, dosage compensation, and differential expression between sexes. To do this we must identify putative sex chromosome scaffolds. In order to accomplish this we assembled the reference genomes, and performed quality control and trimming. We chunked these reference genomes into bite sized pieces and used BWA to map the DNA reads to the reference and processed these BAM files. These are the files that will be fed into gila_chromstats.py.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~gila_chromstats.py~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
This script takes a list of input bam files, casts data from these files into dataframes, and plots the female to male ratio of coverage across scaffolds.

This script requires an input file of count per scaffold per sample. #FIXME? This file comes out of the "rule chromstats dna:". The user can indicate the full path to the file using the flag: --input_file.

--input_file ~/lab_projects/gila1_chrom_stats_count.txt

Along with this input file, it requires the user to input the bam files from males and females separately. The user can add samples using the flags: --male_list and --female_list to indicate the samples sex.

--male_list 'G_10_dna.gila1.mkdup.sorted.bam' 'G_16_dna.gila1.mkdup.sorted.bam' 'G_KI01_dna.gila1.mkdup.sorted.bam' --female_list 'G_30_dna.gila1.mkdup.sorted.bam' 'G_35_dna.gila1.mkdup.sorted.bam' 'G_L_dna.gila1.mkdup.sorted.bam'

 A dataframe containing information from these files will be created. The user should indicate the name of this output file using the flag --output_dataframe. The output will be csv formatted so a .txt extension is recommended. This output will be used in a following script and unpacked using the method read_csv().

 --output_dataframe 'gila_chromstats_df.txt'

 That dataframe is also output as html. The user should name that file using the flag: --output_html.

 --output_html 'gila_chromstats_df.html'

Our data came back with NaN and inf values as well that we wished to be able to remove. A seperate dataframe was collected for these values and is output to html. #FIXME(put in a to_csv as well?)

The user can specify the name of this dataframe using the flag: --output_html_no_nan.

--output_html_no_nan 'gila_chromstats_df_no_nan.html'

Scaffolds that did not meet a certain coverage cutoff value were stripped into their own dataframe. The user should specify this cutoff value using the flag: --coverage_cutoff

--coverage_cutoff '.95'

The user should specify the name of the dataframe of stripped values using the flag: --output_html_cutoff_df .

--output_html_cutoff_df 'df_ratio_less_than.html'

A plot is created of the female to male ratio per scaffold. The user should specify the filename to hold the plot using the flag: --plot_title.

--plot_title 'gila_chromstats_f_m_ratio.png'

An example run of this program is given below.

python gila_chromstats.py --input_file ~/lab_projects/gila1_chrom_stats_count.txt --male_list 'G_10_dna.gila1.mkdup.sorted.bam' 'G_16_dna.gila1.mkdup.sorted.bam' 'G_KI01_dna.gila1.mkdup.sorted.bam' --female_list 'G_30_dna.gila1.mkdup.sorted.bam' 'G_35_dna.gila1.mkdup.sorted.bam' 'G_L_dna.gila1.mkdup.sorted.bam' --output_dataframe 'gila_chromstats_df.txt' --output_html 'gila_chromstats_df.html'  --output_html_no_nan 'gila_chromstats_df_no_nan.html' --coverage_cutoff '.95' --output_html_cutoff_df 'df_ratio_less_than.html' --plot_title 'gila_chromstats_f_m_ratio.png'
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We then used XYalign's CHROM_STATS on these bam files, yielding our '.stats' files. These .stats files are fed as input into gila_statistics_ver2.py.

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~gila_statistics_ver2.py~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This script is used to calculate the reads mapped ratio, The percent of reads that are unmapped, and the estimated coverage. It takes a list of stats files as input. The user can specify the path to these input files using the flag: --input_files

--input_files  G_10_dna.gila1.dna.mkdup.sorted.bam.stats G_16_dna.gila1.dna.mkdup.sorted.bam.stats G_30_dna.gila1.dna.mkdup.sorted.bam.stats G_35_dna.gila1.dna.mkdup.sorted.bam.stats G_KI01_dna.gila1.dna.mkdup.sorted.bam.stats G_L_dna.gila1.dna.mkdup.sorted.bam.stats

The script then casts this data into a dataframe for calculations and outputs that dataframe as html and as csv. The user should name these output files, using the flags --output_csv_df, and --output_html_df respectively.

--output_csv_df gila_statistics_output_df.txt --output_html_df gila_statistics_output_df.html

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~gila_expression.py~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

So now that we have organized our DNA data, we now turn to our RNA data. Our RNA data comes as output from hisat2 which mapped the RNA reads. This was run through stringtie which outputs a series of '.ctab' files which quantify expression. this script takes those files as input. The input files should be specified by using the flag: --input_files

--input_files t_data_10.ctab t_data_16.ctab t_data_30.ctab t_data_35.ctab

This should be followed by the sex of each sample entered in the same order using the flag: --sex

--sex male male female female

The script also requires the reference entered with the flag: --fai

--fai gila2.fasta.fai

The script casts this data into a dataframe, performs calculations, and restructures data. The output is this new dataframe (in csv form) which should be named by the user using the flag: --output_file

--output_file gila_expression_1.txt

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~gila_plot.py~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This script takes the output of gila_expression as input. Its job is to generate a plot of count v.s. female to male FPKM. This plot gives us an idea of the shape of the data as far as RNA transcripts are concerned.

The user should specify the path to the input file using the flag: --input_files

--input_file gila_expression_1.txt

In our RNA data we expect there to be transcripts with near-zero expression or mismatches betweeen sexes, leaving our dataframe with NaN and inf values. These values may or may not be of note later on so we sort them into their own dataframes, and also create a dataframe that omits those transcripts.

The user should name the dataframe containing NaN values using the flag: --nan_html_output

--nan_html_output gila_plot_nan_df.html

The user should name the dataframe containing inf values using the flag: --inf_html_output

--inf_html_output gila_plot_inf_df.html

The output file is a histogram. The user should specify the number of bins (subdivisions) of the histogram using the flag: --num_bins

--num_bins 1000

The histogram is plotted from x = 0 until a value specified by the user. The user should specify this value using the flag: --range

--range 4

The output is a image file, so it should be specified as such using the extension .png. The user may enter the name of this file using the flag --output_file

--output_file gila_plot_figure.png
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~gila_big_dataframe.py~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

So now that we have collected and inspected the data for DNA and RNA, it is useful to compile all of this data into a big datafrme that we can use as reference going forward. This script compiles all of the relevant data going forward in our analysis.

It takes as input the output from gila_chromstats.py and gila_expression.py. These outputs should be in .txt or .csv format as specified above ( because it unpacks them with the method read_csv() ).

The user should specify these files using the flag: --input_files

--input_files 'gila_chromstats_df.txt' 'gila_expression_1.txt'

The output of this script should be specified using the flag: --output_csv_df

--output_csv_df gila_big_dataframe_csv_df.txt

The script also throws the dataframe to html for easy inspection. The user should specify the name of this file as well using the flag: --output_html_df

--output_html_df gila_big_dataframe_html_df.html
