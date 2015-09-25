import pandas
import gzip
import shlex
import urllib

'''
Functions for parsing common bioinformatics file formats.
Returns pandas dataframe objects.
Dependencies: pandas, gzip, shlex, urllib
'''

def gff3parser( myfile ):
    '''parses gff3 files and returns pandas dataframe.
    input file can be gzipped.
    '''
    if myfile.endswith('.gz'):
        filehandle = gzip.open( myfile )
    else:
        filehandle = open( myfile )

    data = pandas.read_table(filehandle, 
                             sep = '\t',
                             comment = '#',
                             skip_blank_lines = True,
                             names = ['seqid','source','feature',
                                 'start','end','score','strand',
                                 'frame','attributes'],
                             converters = { 'attributes':
                                           lambda x:
                                           dict(
                                           tuple(y.split('=')) for y in
                                           x.split(";")
                                           )
                                          }
                            )
    data['attributes'] = data['attributes'].apply( lambda attribute:
                                {key:urllib.unquote(attribute[key])
                                            for key in attribute}
                                             )
    return data

def gff2parser( myfile ):
    '''parses gff2 files and returns pandas dataframe.
    input file can be gzipped.
    '''
    if myfile.endswith('.gz'):
        filehandle = gzip.open( myfile )
    else:
        filehandle = open( myfile )

    data = pandas.read_table(filehandle, 
                             sep = '\t',
                             comment = '#',
                             skip_blank_lines = True,
                             names = ['seqid','source','feature',
                                 'start','end','score','strand',
                                 'frame','attributes'],
                             converters = { 'attributes':
                                           lambda x:
                                           dict(
                                                tuple(shlex.split(y))
                                                for y in x.split(";")
                                                )
                                          }
                            )
    data['attributes'] = data['attributes'].apply( lambda attribute:
                                {key:urllib.unquote(attribute[key])
                                            for key in attribute}
                                             )
    return data
