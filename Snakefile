# Adapt to your own selection of chromosomes
chromosomes = [9,]

rule all:
    input:
        expand("data/extracted_genotypes/chr{chrom}/genotypes_encoded.txt", chrom=chromosomes),


rule encode_genotypes:
    input:
        genotypes="data/extracted_genotypes/chr{chrom}/genotypes.txt",
        samples="data/extracted_genotypes/chr{chrom}/samples.txt",
    output:
      encoded="data/extracted_genotypes/chr{chrom}/genotypes_encoded.txt",
    shell:
        "python scripts/encode_genotypes.py"
        " --fn_genotypes {input.genotypes}"
        " --fn_samples {input.samples}"
        " --fn_output {output.encoded}"


rule query_genotypes:
    input:
        selected_pos="data/selected_genotypes/genotypes_chr{chrom}.tsv",
        vcf_file="/projects/ukbiobank-AUDIT/data/imputed_genotype/cur/vcf/ukb32683_imp_chr{chrom}_v3.vcf.gz"
    output:
        genotypes="data/extracted_genotypes/chr{chrom}/genotypes.txt",
        samples="data/extracted_genotypes/chr{chrom}/samples.txt"
    envmodules:
        "perl",
        "gsl/2.5",
        "bcftools/1.20"
    shell:
        """
        bcftools query --regions-file {input.selected_pos} {input.vcf_file} --format '%CHROM\t%POS\t%REF\t%ALT[\t%GT]\n' -o {output.genotypes}
        bcftools query --list-samples {input.vcf_file} > {output.samples}
        """