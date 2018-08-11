import os
myfiles = [
'G_10_dna.gila1.dna.mkdup.sorted.bam.stats',
'G_16_dna.gila1.dna.mkdup.sorted.bam.stats',
'G_30_dna.gila1.dna.mkdup.sorted.bam.stats',
'G_35_dna.gila1.dna.mkdup.sorted.bam.stats',
'G_KI01_dna.gila1.dna.mkdup.sorted.bam.stats',
'G_L_dna.gila1.dna.mkdup.sorted.bam.stats'
]
#put fome parseargs here to input files.

class_list = []
def make_names():
    for file in myfiles:
        samplename = file.split('.gila1.')[0] #stores a new string variable
        class_list.append(str(samplename))

def make_class():
    for x in class_names:
        x = Gila()

def pop_class():
    for x in myfiles:
        with open(x,'r') as readfile:
            for classname in class_names:
                if readfile.starstwith(classname):
                    for line in readfile:


class Gila:
    def __init__(self):
        print('class instantiated.')
    def print_sequences(self):
        print(self.sequences)

# for file in myfiles:
#     samplename = file.split('.gila1.')[0] #stores a new string variable
#     print('printing samplename:', samplename)
#     samplename = Gila() #turns the string into a class
#     print('checking if samplename is now a class', samplename)
#     with open(file,'r') as readfile:
#         for line in readfile:
#             key, value = line.split(':')
#             samplename.key = value #is this not working? How can I check??
# G_L_dna.print_sequences()
#
#
class_list = []
for x in class_list:
    x = Gila()
    for x in myfiles:
        with open(f,'r') as readfile:
            for line in readfile:
