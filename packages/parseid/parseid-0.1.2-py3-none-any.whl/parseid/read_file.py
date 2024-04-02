
from typing import Iterable

class ReadFile:
    def __init__(self, infile:str):
        self.infile = infile
    
    def text(self, has_header:bool=True, sep:str='\t') -> Iterable:
        with open(self.infile, 'rt') as f:
            if has_header:
                next(f)
            for line in f:
                items = line.rstrip().split(sep)
                yield items

    def gene_refseq_uniprotkb_collab(self) -> Iterable:
        '''
        read "gene_refseq_uniprotkb_collab" downloaded from NCBI
        '''
        with open(self.infile, 'rt') as f:
            next(f)
            for line in f:
                items = line.rstrip().split('\t')
                yield items
