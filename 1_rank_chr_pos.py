# %%
from pathlib import Path
import pandas as pd

fname = 'data/combined_gwas.csv'  # adapt to file destination
# fname = '../pan_ukbiobank_gwas/data/combined_gwas.csv'
folder_out = 'extract_genotypes'

TOP_N = 100

# %%
folder_out = Path(folder_out)
folder_out.mkdir(exist_ok=True)


# %%
df = (pd
      .read_csv(fname, index_col=[0, 1], low_memory=False)
      .astype('float16')
      )
df

# %% [markdown]
# Rank positions by the maximum value of the GWAS statistics across all phenotypes.
# - adapt to other selection criteria if needed.

# %%
ranked_positions = df.max(axis=1).sort_values(ascending=False)

# %% [markdown]
# Use the TOP_N positions to extract genotypes.

# %%
ranked_positions.index[:TOP_N]

# %%
selected = (ranked_positions
            .index[:TOP_N]
            .to_frame()
            .sort_index())
selected.to_csv(folder_out / 'chr_pos.tsv',
                index=False,
                header=False)

# %% [markdown]
# Save positions to extract genotypes from per chromosome as the UK Biobank data is
# split by chromosome.

# %%
for chr, _df_chr in selected.groupby(level='chr'):
    fname = folder_out / f'genotypes_chr{chr}.tsv'
    _df_chr.to_csv(fname,
                   sep='\t',
                   header=False,
                   index=False)

# %%
