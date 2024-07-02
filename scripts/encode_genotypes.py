"""
Parse Genotypes and encode as integers 0, 1, 2.

```tsv
1	66121781	G	T	1/1	0/1	1/1	0/1	0/0
```

Will be encoded as:

```tsv
chrom 1
pos 66121781
ref G
alt T
sample1 2
sample2 1
sample3 2
sample4 1
sample5 0
```

"""
from pathlib import Path
import numpy as np
import pandas as pd
import argparse


def apply_int(x):
    try:
        return int(x)
    except ValueError:
        return 0


def main(args):

    samples = pd.read_csv(args.fn_samples, header=None).squeeze().to_list()

    index = list()
    data = list()

    with open(args.fn_genotypes) as f:

        for line in f:
            line = line.strip().split('\t')
            chrom, pos, ref, alt = line[:4]

            genotypes = line[4:]
            genotypes = [sum(map(apply_int, g.split('/'))) for g in genotypes]
            data.append(pd.Series(np.array(genotypes, dtype='int8'),
                        name=(chrom, pos, ref, alt)))
            index.append([chrom, pos, ref, alt])

    df = pd.concat(data, axis=1)
    df.columns.names = ('chrom', 'pos', 'ref', 'alt')
    df.index = samples
    df.to_csv(args.fn_output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Parse Genotypes')
    parser.add_argument('--fn_genotypes', '-g',
                        type=str, help='genotypes file')
    parser.add_argument('--fn_samples', '-s', type=str,
                        help='sample identifiers')
    parser.add_argument('--fn_output', '-o', type=str, help='output file')
    args = parser.parse_args()
    main(args)
