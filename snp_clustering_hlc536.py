import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.cluster import KMeans, DBSCAN, kmeans_plusplus, AgglomerativeClustering
from scipy.spatial.distance import cdist


#folder_out = '/projects/ukbiobank-AUDIT/people/hlc536/genomics/step2/data/selected_genotypes'
folder_out = None # insert your folder here
folder_out = Path(folder_out)
folder_out.mkdir(exist_ok=True)

# Load result from first step, modify indices
# combined_gwas_path = '/projects/ukbiobank-AUDIT/people/hlc536/genomics/step1/combined_gwas.csv'
combined_gwas_path = None # insert your path here
combined_gwas = (pd
      .read_csv(combined_gwas_path, index_col=[0, 1], low_memory=False)
      )
df_reset = combined_gwas.reset_index()
df_reset['nidx'] = range(len(df_reset))
combined_gwas = df_reset.set_index(['chr', 'pos', 'nidx'])

# Fill nans with zeros
full = combined_gwas.fillna(0).to_numpy()

# DBSCAN clustering -> modify parameters if needed
dbs_labels = DBSCAN(eps=5, min_samples=3).fit_predict(full)

num_labels = len(set(dbs_labels))
noisy = np.sum(dbs_labels == -1)
noisy_ratio = noisy/len(dbs_labels)
print(f'number of labels: {num_labels}, number of outliers: {noisy}, ratio={noisy_ratio}')

# Initialize an empty list to store representative samples
representative_samples = []
representative_idx = []

# Loop through each cluster (ignoring noise, labeled as -1)
for cluster_label in set(dbs_labels):
    if cluster_label != -1:  # Ignore noise
        # Get indices of the points in the current cluster
        cluster_indices = np.where(dbs_labels == cluster_label)[0]
        
        # Extract points of the current cluster
        cluster_points = full[cluster_indices]
        
        # Calculate the centroid of the cluster
        centroid = cluster_points.mean(axis=0)
        
        # Find the point closest to the centroid
        distances = cdist([centroid], cluster_points, metric='euclidean')
        closest_point_idx = np.argmin(distances)
        
        # Store the index of representative point
        representative_idx.append(cluster_indices[closest_point_idx])

# With or without outliers...
chosen = representative_idx #+ outliers
chosen.sort()
filtered_df = combined_gwas.iloc[chosen, :].index.to_frame().sort_index()
filtered_df = filtered_df.drop(columns=['nidx'])

# Write selected SNPs to csv file
filtered_df.to_csv(folder_out / 'chr_pos_selected.tsv',
                index=False,
                header=False)

# Write one csv file per chromosome
for chr, _df_chr in filtered_df.groupby(level='chr'):
    fname = folder_out / f'genotypes_chr{chr}.tsv'
    _df_chr.to_csv(fname,
                   sep='\t',
                   header=False,
                   index=False)