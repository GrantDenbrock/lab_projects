#for sample in sample list
#and for each transcript in the sample_list
#determine if sample is male or female using tags
#then seperate and place values accordingly
#if the transcript exists in transcript_dict
#just append its values for FPKM and stuff
#else append the new transcript number and also do its values of FPKM and stuff.

#might need to cut columns into lists like the other project. FIXME
import os

sample_list = []
males = []
females = []
transcript_dict = {}
data_dict = {}

#so the structure is... data_dict has Key: transcript number and Value: another dictionary with Key: parameter and Value: Value
#so when I go data_dict[transcript number[parameter]] --> I get out the value that I want. Do I want to be able to get the value per lizard? FIXME
#lets say no for mow and just get something working.

#CREATE SAMPLE LIST
files = [f for f in os.listdir('.') if os.path.isfile(f)]
for f in files:
    if f.endswith('.stats')==True:
        sample_list.append(f)
print('printing sample list:')
print(sample_list)

#do you want to sort by male or female?
#implement a --sort flag that will iterate samples in sample list and allow you to say whether is male or female FIXME

#fill in transcripts lists
transcrpits = []
files = [f for f in os.listdir(os.curdir) if os.path.isfile(f)] # creates a list of files in current directory
#print(files)
for f in files: #for each file in current directory
    if f.endswith('.transcripts.txt')==True: #and if it ends with .data.txt
        with open(f , 'r') as readfile: #open the file f as readfile
            for line in readfile: #for value in the readfile
                transcript=line.strip() #variable number can take the value of the line without all the bullshit newline characters #also need to get rid of the quotations, turning string into float.
                #print(number)
                transcripts.append(transcript)
#and do the same for the other columns that we want in our data table
