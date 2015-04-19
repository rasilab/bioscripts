import pandas
import gzip
import shlex
import urllib

'''
Functions for parsing common bioinformatics file formats.
Returns pandas dataframe objects.
'''

def gff3parser( myfile ):
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
                                           {y.split('=') for y in
                                           x.split(";")}
                                          }
                            )
    return data

def gff2parser( myfile ):
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
