# This script will take as first input a fastq.gz file 
# that contains unaligned indices.
# The subsequent arguments can be all the indices in the
# experiment that you want to demultiplex.
# Separate each index by a space

import sys  # for getting command line arguments
from Bio import SeqIO  # for bio sequence file input output
import gzip  # for read write gzipped files

inputfile = sys.argv[1]  # fastq file with unaligned indices
indices = sys.argv[2:]  # these are the indices used in your expt

# open fastq file for reading
records = SeqIO.parse(gzip.open(inputfile), 'fastq')
numberOfProcessedReads = 0  # keep track of how many reads are processed

# open an output file for each index
outputFiles = dict((index, gzip.open(index + '_' + inputfile, 'w'))
                   for index in indices)

# iterate through fastq records
for read in records:
    # the 10th col separated by : is the index
    index = read.description.split(':')[9]
    if index in indices:  # if index in your list of indices, write it
        SeqIO.write(read, outputFiles[index], 'fastq')
    # print every nth record processed
    if numberOfProcessedReads % 100000 == 0:
        print(numberOfProcessedReads)
    numberOfProcessedReads += 1

for File in outputFiles.values():
    File.close()
