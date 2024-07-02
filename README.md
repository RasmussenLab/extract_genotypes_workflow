# Extract Genotypes

Based on selected snps, extract genotypes from VCF files.

## SNP selection using Pan-UKB

- in case one selected the Pan-UKB GWAS for SNP selection, the `combined_gwas.csv` file
from thw `pan_ukbiobank_gwas` workflow needs to be used to select the SNPs and save their 
position in [`data/selected_positions`](data/selected_positions/README.md) with the help of 
[`1_rank_chr_pos.py`](1_rank_chr_pos.py)

## Run the Snakemake workflow

Uses `bcftools/1.20` environment module on our cluster.

```
snakemake -c1 --use-envmodules -n  # dry-run
snakemake -c1 --use-envmodules  #  run with one core
```

## Manuel example

Uses the imputed vcf files under `/datasets/ukb_32683-AUDIT/genotype/cur/vcf/`.

```bash
# Load bcftools
module load perl/5.38.0 gsl/2.5  bcftools/1.20
# Extract genotypes
VCF_FILE=/datasets/ukb_32683-AUDIT/genotype/cur/vcf/ukb32683_cal_chr1_v2.vcf.gz
bcftools query --regions-file chr_pos.tsv $VCF_FILE --format '%CHROM\t%POS\t%REF\t%ALT[\t%GT]\n' > chr1_genotypes.tsv
# Extract imputed genotypes
VCF_FILE=/datasets/ukb_32683-AUDIT/imputed_genotype/cur/vcf/ukb32683_imp_chr1_v3.vcf.gz
bcftools query --regions-file chr_pos.tsv $VCF_FILE --format '%CHROM\t%POS\t%REF\t%ALT[\t%GT]\n' > chr1_genotypes.tsv
bcftools query --list-samples $VCF_FILE > samples.txt
```
