# Variant Calling from Nanopore Sequencing

SNV, SV and CNV calling, modified base calling, and STR genotyping of human samples ([epi2me-labs/wf-human-variation](https://github.com/epi2me-labs/wf-human-variation))

Oxford Nanopore Technologies provides an analysis workflow for the analysis of genomic variants
from long-read nanopore sequencing data.
This analysis workflow includes:

- diploid variant calling (Clair3)
- structural variant calling (Sniffles2)
- copy number variant calling (Spectre or QDNAseq)
- short tandem repeat (STR) expansion genotyping (Straglr)
- analysis of modified base calls

> Please note, this pipeline is intended for use with 20x whole-genome Oxford Nanopore Technologies
sequencing data (with the exception of QDNAseq, please see this section for more information).
Usage outside of this (e.g. with adaptive sampling data, or using lower coverage inputs) may
cause the workflow to terminate with an error, or produce unexpected results.

Workflow repository: [epi2me-labs/wf-human-variation](https://github.com/epi2me-labs/wf-human-variation)

## Inputs

Nanopore sequencing data should be uploaded as either Unaligned BAM, or as Nanopore Sequencing POD5.
If POD5 files are uploaded, they should be processed by the Dorado basecalling pipeline prior to analysis
for variant calling.

## Outputs

Output files may be aggregated including information for all samples or provided per sample. Per-sample files will be prefixed with respective aliases and represented below as {{ alias }}.

| Title | File path | Description | Per sample or aggregated |
|-------|-----------|-------------|--------------------------|
| Report of the alignment statistics | {{ alias }}.wf-human-alignment-report.html | Report summarising the results of the alignment statistics for the sample. | per-sample |
| JSON file of some base statistics | {{ alias }}.stats.json | This JSON file contains base statistics on the reads, mappings, SNPs and SVs for the sample. | per-sample |
| Report of the SNP workflow | {{ alias }}.wf-human-snp-report.html | Report summarising the results of the SNP subworkflow for the sample. | per-sample |
| Report of the SV workflow | {{ alias }}.wf-human-sv-report.html | Report summarising the results of the SV subworkflow for the sample. | per-sample |
| Report of the CNV workflow | {{ alias }}.wf-human-cnv-report.html | Report summarising the results of the CNV subworkflow for the sample. | per-sample |
| Report of the STR workflow | {{ alias }}.wf-human-str-report.html | Report summarising the results of the short tandem repeat subworkflow for the sample. | per-sample |
| Short variant VCF | {{ alias }}.wf_snp.vcf.gz | VCF file with the SNPs for the sample. | per-sample |
| Structural variant VCF | {{ alias }}.wf_sv.vcf.gz | VCF file with the SVs for the sample. | per-sample |
| Structural variant SNF | {{ alias }}.wf_sv.snf | SNF file with the SVs for the sample, for onward multi-sample SV calling. | per-sample |
| Copy number variants VCF | {{ alias }}.wf_cnv.vcf.gz | VCF file with the CNV for the sample. | per-sample |
| Modified bases BEDMethyl | {{ alias }}.wf_mods.bedmethyl.gz | BED file with the aggregated modification counts for the sample. | per-sample |
| Modified bases BEDMethyl (haplotype 1) | {{ alias }}.wf_mods.1.bedmethyl.gz | BED file with the aggregated modification counts for haplotype 1 of the sample. | per-sample |
| Modified bases BEDMethyl (haplotype 2) | {{ alias }}.wf_mods.2.bedmethyl.gz | BED file with the aggregated modification counts for haplotype 2 of the sample. | per-sample |
| Modified bases BEDMethyl (ungrouped) | {{ alias }}.wf_mods.ungrouped.bedmethyl.gz | BED file with the aggregated modification counts of non-haplotagged reads for the sample. | per-sample |
| Short tandem repeat VCF | {{ alias }}.wf_str.vcf.gz | VCF file with the STR sites for the sample. | per-sample |
| Alignment file | {{ alias }}.cram | CRAM or BAM file with the aligned reads for the sample, generated when the input file is unaligned. | per-sample |
| Alignment file index | {{ alias }}.cram.crai | The index of the resulting CRAM or BAM file with the reads for the sample, generated when the input file is unaligned. | per-sample |
| Haplotagged alignment file | {{ alias }}.haplotagged.cram | CRAM or BAM file of all input reads with haplotags added by phasing. | per-sample |
| Haplotagged alignment file index | {{ alias }}.haplotagged.cram.crai | The index of the resulting CRAM or BAM file produced when haplotags have been added by phasing. | per-sample |
| Mean coverage for each region | {{ alias }}.regions.bed.gz | The mean coverage in the individual regions of the genome in BED format. | per-sample |
| Coverage per region above the given thresholds | {{ alias }}.thresholds.bed.gz | The BED reporting the number of bases in each region that are covered at or above each threshold values (1x, 10x, 20x and 30x). | per-sample |
| Distribution of the proportion of total bases covered by a given coverage value | {{ alias }}.mosdepth.global.dist.txt | The cumulative distribution indicating the proportion of total bases covered by a given coverage value, both genome-wide and by sequence. | per-sample |
| Mean coverage per sequence and target region | {{ alias }}.mosdepth.summary.txt | The summary of mean depths per chromosome and within specified regions per chromosome. | per-sample |
| BEDgraph of the single-base coverage | {{ alias }}.per-base.bedgraph.gz | The single-base coverage of the genome in BED graph format. | per-sample |
| Gene level coverage summary | SAMPLE.gene_summary.tsv | A table where each gene of the input BED file has columns describing the percentage of positions along the gene region that are covered to a given threshold, and a column with the average coverage. | per-sample |
| Haplocheck contamination summary | {{ alias }}.haplocheck.tsv | A table generated by [haplocheck](https://mitoverse.readthedocs.io/haplocheck/haplocheck/), with estimate of contamination from the MT genome. | per-sample |
| FAI index of the reference FASTA file | {{ ref }}.fai | FAI Index of the reference FASTA file. | aggregated |
| GZI index of the reference FASTA file | {{ ref }}.gzi | GZI Index of the reference FASTA file. | aggregated |
