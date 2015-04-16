from Bio.SeqIO.QualityIO import FastqGeneralIterator

bases = ['A', 'C', 'T', 'G']

indexdict = dict()
originalindices =  ['GGCCAC', 'TAGTTG', 'CCGGTG', 'ATCGTG', 'CGAAAC', 'CGTACG',
                    'CCACTC', 'GCTACC', 'ATCAGT', 'GCTCAT', 'AGGAAT', 'CTTTTG']

for index in originalindices:
    for position in range(len(index)):
        for base in bases:
            if index[position] == base: 
                continue
            newindex = index[:position] + base + index[position+1:]
            indexdict[newindex] = index
    

recordIterator = FastqGeneralIterator( open( '../rawfastq/Undetermined_S0.R1.fastq', 'r' ) )

numberOfProcessedReads = 0

outputFiles = dict((index,open(index + '_extra.fastq','w')) for index in oldindices)

for title, seq, qual in  recordIterator: #look at a fastq file for example of these lines.
    numberOfProcessedReads += 1
    newindex = title.split(':')[9]
    if newindex in indexdict:
        outputFiles[ indexdict[newindex] ].write("@%s\n%s\n+\n%s\n" % (title, seq, qual)) #format string for writing in fastq format.
    if numberOfProcessedReads % 100000 == 0:
        print numberOfProcessedReads
        
for File in outputFiles.values():
    File.close()
