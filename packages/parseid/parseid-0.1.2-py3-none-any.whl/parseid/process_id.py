"""
data structure: The di-trie. Here are the features:
Define A trie and B trie:
one leave node of A trie is mapped to one or more leave nodes of B trie
"""
from .read_file import ReadFile
from .trie import Trie
from .ditrie import DiTrie

class ProcessID:
    def __init__(self, infile:str):
        self.infile = infile
    
    def uniprotkb_protein_accession(self) -> Trie:
        """
        source file: gene_refseq_uniprotkb_collab downloaded from NCBI/Entrez
        suck UniProtKB protein accession numbers
        """
        acc_trie = Trie()
        n = 0
        self.records = ReadFile(self.infile).gene_refseq_uniprotkb_collab()
        for items in self.records:
                acc = items[1]
                acc_trie.insert(acc)
                n += 1
        print(f"Total number of {n} UniProtKB protein accession numbers are fed into Trie.")
        return acc_trie

    def ncbi_protein_accession(self) -> Trie:
        """
        source file: gene_refseq_uniprotkb_collab downloaded from NCBI/Entrez
        suck NCBI protein accepython setup.pyssion numbers
        """
        acc_trie = Trie()
        n = 0
        self.records = ReadFile(self.infile).gene_refseq_uniprotkb_collab()
        for items in self.records:
            acc = items[0]
            acc_trie.insert(acc)
            n += 1
        print(f"Total number of {n} NCBI protein accession numbers are fed into Trie.")
        return acc_trie


    def map_ncbi_uniprotkb(self) -> DiTrie:
        '''
        source file: gene_refseq_uniprotkb_collab downloaded from NCBI/Entrez
        map: UniProtKB accession number ~ NCBI protein accession number
        '''
        uniprotkb_acc_trie = Trie()
        ncbi_acc_trie = Trie()
        map_trie = DiTrie(uniprotkb_acc_trie, ncbi_acc_trie)

        n = 0
        self.records = ReadFile(self.infile).gene_refseq_uniprotkb_collab()
        for items in self.records:
            ncbi_acc, uniprotkb_acc = items[:2]
            map_trie.insert(ncbi_acc, uniprotkb_acc)
            n += 1
        return map_trie
    

