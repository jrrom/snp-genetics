import numpy as np

def snp_factory(nucleotides):
    def go(linelist):
        final_list = []
        for line in linelist:
            # We do outer comparison for each nucleotide
            mask = (line[:, np.newaxis] == nucleotides)
            rowmask = mask.T
            index_mask = rowmask * np.arange(len(line))
            
            # n [nA, nG, nT, nC]
            n = np.sum(mask, axis=0)
        
            # T [tA, tG, tT, tC]
            T = np.sum(index_mask, axis=1)
        
            # To calculate variance, baseline is 0 due to zeros_like
            mu = np.zeros_like(T, dtype=float)
            np.divide(T, n, out=mu, where=n != 0)
        
            D = np.zeros_like(T, dtype=float)
            numerator = np.square(index_mask - mu[:, np.newaxis]) * rowmask
            np.divide(np.sum(numerator, axis=1), n, out=D, where=n != 0)
        
            final_list.append(np.stack([n, T, D], axis=1).flatten())
        return np.array(final_list)
    return go

snp_single = snp_factory(["A", "T", "G", "C"])
snp_double = snp_factory(["AA", "TT", "GG", "CC"])
    
    
        
