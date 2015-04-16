#!/usr/bin/env python

# Python Modules
import re #regular expression library.
import sys #to read in data filename from the command line.
import gzip #library to handle gzipped files.
from Bio.SeqIO.QualityIO import FastqGeneralIterator #for iterating through 
														#fasta records.

# Adjustable Parameters
inputFile = sys.argv[1]
outputFile = open(sys.argv[2], 'w')
numberOfAs = 10 #only reads having these many contiguous As are written 
				#to output. the trimming will happen at the first such
				#polyA run if there are multiple runs.
extraTrimmingLength = 0 #these many nts are removed from the 5' side 
						#of the polyA run.
end5TrimmingLength = 0 #these many nts are removed from the 5' end of the read.
remainingLength = 13 #only reads longer than these many nts are 
					#written to output.

recordIterator = FastqGeneralIterator( gzip.open( inputFile, 'r' ) ) # open 
					#input file for iterating through reads sequentially
numberOfProcessedReads = 0
numberOfCountedReads = 0
for title, seq, qual in  recordIterator: #look at a fastq file 
											#for example of these lines.
    numberOfProcessedReads += 1
    stopLocation = re.search( 'A{' + str(numberOfAs) + ',}', seq ) #identifies 
								#reads with a run of >=numberOfAs adenines.
    if stopLocation is None: #discard reads that do not 
								#have >=numberOfAs adenine stretch.
        continue
    trimStop = stopLocation.start() - extraTrimmingLength - 1 # trims the 
				#'extraTrimmingLength' number of nt 5' to the polyA tail.
    if trimStop < remainingLength: # ignores trimmed reads that are 
									#less than 'remainingLength' nt long.
        continue
    outputFile.write("@%s\n%s\n+\n%s\n" % (title, 
									seq[end5TrimmingLength:trimStop + 1], 
						qual[end5TrimmingLength:trimStop + 1])) # write the 5' 
								#end trimmed read to the output file.
    numberOfCountedReads += 1
outputFile.close()

print( '%d : Total number of processed reads'%numberOfProcessedReads)
print( '%2.2f : Percent of reads that passed threshold' % 
			( numberOfCountedReads / float( numberOfProcessedReads ) * 100 ))

