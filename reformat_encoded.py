from pathlib import Path
import pandas as pd
import numpy as np

# in_path = '/projects/ukbiobank-AUDIT/people/hlc536/genomics/step2'
in_path = None # add your folder here

for chrn in [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,'X']:
    df = pd.read_csv(f'{in_path}/data/extracted_genotypes/chr{chrn}/genotypes_encoded.txt', sep=',', header=[1])
    df2 = df.drop([0,1]).rename(columns={'pos':'f.eid'})
    df2.columns = [df2.columns[0]] + [f'chr{chrn}_' + col for col in df2.columns[1:]]
    df2.to_csv(f'{in_path}/data/extracted_genotypes/chr{chrn}/chr{chrn}_prep.tsv', sep='\t', index=False)