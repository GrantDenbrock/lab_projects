import os
import numpy as np

sample_list = [] #will populate this with actual files. SO now that we have RNA data sample list will contain RNA stats as well.

parameters = [] #comes from the cut -f 1 of stats file

data = [] #comes from cut -f 2 of stats file



#make main dictionary
gilas = {} # do I want to make this an ordered dict? I don't think it matters too much. Not going to look at the order I added things am I?

#now we just need to read in the files (file1 and file_b) in the right format and we are off to the races.
# this block takes all files in current directory matching the pattern: .stats , and adds them to a list
files = [f for f in os.listdir('.') if os.path.isfile(f)]
for f in files:
    if f.endswith('.stats')==True:
        sample_list.append(f)
print('printing sample list:')
print(sample_list)

#do I want seperate RNA and DNA sample lists? Or would it be fine just to run them all the same way?
#pros: not having to rewrite chunks of code
#cons: will have to parse later to use the data, but that seems pretty easy using bash since I can grep rna.


#now we just need to read in the files (file1 and file_b) in the right format and we are off to the races.
# this block takes files in the current directory that match the pattern parameters.txt and puts the contents into a list
#the resulting list is a list of parameters of the stats file for use in the dictionary
files = [f for f in os.listdir('.') if os.path.isfile(f)]
print('printing files')
print(files)
for f in files:
    if f.endswith('parameters.txt')==True:
        with open(f , 'r') as readfile:
            for line in readfile:
                parameter = line.strip()
                if parameter != '':
                    parameters.append(parameter)
#throwing an error because the rna lists didnt come with a params file. Did the DNA come with a params file? FIX ME<------------------
#maybe the easy way to fix is for each rna file append parameters.txt? Really would like to get some version control going. 
#print(parameters)
#print(len(parameters))
#print('printing parameters list:')
#print(parameters[0]) >> raw total sequences:



#now we just need to read in the files (file1 and file_b) in the right format and we are off to the races.
#this block makes the list: data
# each of the .data.txt files contain the corresponding data for the parameters
files = [f for f in os.listdir(os.curdir) if os.path.isfile(f)] # creates a list of files in current directory
#print(files)
for f in files: #for each file in current directory
    if f.endswith('.data.txt')==True: #and if it ends with .data.txt
        with open(f , 'r') as readfile: #open the file f as readfile
            for line in readfile: #for value in the readfile
                number=line.strip() #variable number can take the value of the line without all the bullshit newline characters #also need to get rid of the quotations, turning string into float.
                #print(number)
                data.append(number) #append the value of variable number onto the list data. This is the error in logic. Do we want to make a new list for each sample or do we want to write these all to seperate text files?

#formatting data from string to numerical values
#I need some to remain ints, and some will require floats with several decimal places. Can I just do all to float? Will that mess up the other values by rounding?
#data = list(map(int,data)) NO

for item in data:
    float(item)

#print('printing data list:')
#print(data)
#print(len(data))
#the problem with this strategy is that it puts all the data into one list!
#it would be better if each sample had its own list associated with it. Then when calling the list into the dictionary we could call the list by name?

counters = []
for counter in range(0,len(data)):
    counters.append(counter)

#make and populate all the sub dictionaries
start = 0

for x in sample_list:
    gilas[x]={}
    gilas[x]['data']={}

    for y in range(0,len(parameters)):
        #print(y,start,start + len(parameters))
        gilas[x]['data'][parameters[y]] = {}
        gilas[x]['data'][parameters[y]] = data[y+start] #woohoo!
    start += len(parameters)
print('printing entire gilas dictionary:')
print(gilas)
#f=open(gilas_dictionary.txt, "w+") #create a text file for this all to go into
#f.close()

#print(gilas['G_10_dna.gila1.dna.mkdup.sorted.bam.stats'])

#Ok so now that we can populate our dictionary just like that, we can automate some calculations...
print(gilas[sample_list[1]]['data'][parameters[0]]) #example of usage; will print the characteristic for the lizard in question
print(gilas[sample_list[1]]['data']) #another example of usage; will print all characteristics for the lizard in question
print(gilas[sample_list[1]]) #a stupid example; does same as above except makes the word 'data' visible.
# I do see a flaw that I might have to memorize which order the lizards are in. I hate memorizing things. FIX ME!<-------------

#PARAMETERS FOR REFERENCE~~~~~~~~~~~~~~~~~~~~~~~~~
 #0. ‘raw total sequences:',
 #1.  'filtered sequences:',
 #2. ’sequences:',
 #4. ’1st fragments:',
 #5. ’last fragments:',
 #6. ’reads mapped:',
 #7. ’reads mapped and paired:',
 #8. ’reads unmapped:',
 #9. ’reads properly paired:',
 #10. ’reads paired:',
 #11. 'reads duplicated:',
 #12. ’reads MQ0:',
 #13. ’reads QC failed:',
 #14. 'non-primary alignments:',
 #15. ’total length:',
 #16. ’bases mapped:',
 #17. ’bases mapped (cigar):',
 #18. ’bases trimmed:',
 #19.  'bases duplicated:',
 #20.  'mismatches:',
 #21. ’error rate:',
 #22. ’average length:',
 #23.  'maximum length:',
 #24. ’average quality:',
 #25. ’insert size average:',
 #26. ’insert size standard deviation:',
 #27. ’inward oriented pairs:',
 #28. ’outward oriented pairs:',
 #29. ’pairs with other orientation:',
 #30. ’pairs on different chromosomes:'
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#example calculation:
x=0
while(x < int(len(sample_list))):
    #print(gilas[sample_list[x]]['data'][parameters[20]])
    #print(gilas[sample_list[x]]['data'][parameters[22]])
    num20 = int(gilas[sample_list[x]]['data'][parameters[20]])
    num22 = int(gilas[sample_list[x]]['data'][parameters[22]])
    #print(num20 + num22)
    x=x+1


#going to calculate coverage for each lizard
# using the equation coverage = ('average length')('reads mapped')/('total length')
coverages = []
x=0
while(x < int(len(sample_list))):
    N = int(gilas[sample_list[x]]['data'][parameters[6]])
    L = int(gilas[sample_list[x]]['data'][parameters[22]])
    G = int(gilas[sample_list[x]]['data'][parameters[15]])
    C = N*L/G
    coverages.append(C)
    x=x+1
print("coverages:")
print(coverages)
#gonna need to add coverages to parameters, and then to gilas dictionary if we are going to include this data.
#OR option two is to write calculations to a seperate file!
# we are going to want to make sure that the values of coverage are above a threshold, do I want to do that here or later in R. Probably later in R because I can tweak params more easily by hand after reviewing the data.
# should also be easy to add these to the dictionary as done above for parameters and data lists

#calc percent properly paired
x=0
percent_properly_paired = []
while(x < int(len(sample_list))):
    P = int(gilas[sample_list[x]]['data'][parameters[9]])
    Q = int(gilas[sample_list[x]]['data'][parameters[6]])
    R = 100*P/Q
    percent_properly_paired.append(R)
    x=x+1
print("percent properly paired")
print(percent_properly_paired)

#calc percent duplication
x=0
percent_reads_duplicated = []
while(x < int(len(sample_list))):
    P = int(gilas[sample_list[x]]['data'][parameters[11]])
    Q = int(gilas[sample_list[x]]['data'][parameters[6]])
    R = 100*P/Q
    percent_reads_duplicated.append(R)
    x=x+1
print("percent duplication")
print(percent_reads_duplicated)

# I want to make a function that can pull data for me in a less abstract way
def get_data(sample_number, parameter_number):
        value = float(gilas[sample_list[sample_number]]['data'][parameters[parameter_number]])
        print("getting data for sample " + str(sample_number))
        print(value) #should be float probably. Any problems with using float?
        #should return value so I can use it! waiting to figure out version control before making too many changes.

#EXPECTED COVERAGE, testing the get_data function.
expected_coverages = []
for sample in range(0,len(sample_list)):
    G = get_data(sample,15)
#print(G)
#get_data works pretty good.
