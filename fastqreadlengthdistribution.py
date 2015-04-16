'''Returns a python dictionary with a key for each read length and
a value corresponding to the number of reads of that length.
Also prints the corresponding dictionary'''

import itertools
import gzip
import sys

def fastq_readlength_distribution( myfile ):
    readcount = 0
    readlengths = dict()
    with gzip.open(files[0],"rb") as myfile:
        for read in itertools.islice(myfile,1,None,4):
            length = len(read.strip())
            if length in readlengths:
                readlengths[length] += 1
            else:
                readlengths[length] = 1
            readcount += 1
    print( "%d reads processed"%readcount )
    print( readlengths )
    return( readlengths )
