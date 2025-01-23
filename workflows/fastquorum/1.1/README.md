## Generate Consensus Reads from UMIs (nf-core/fastquorum)

Pipeline to produce consensus reads using unique molecular indexes/barcodes (UMIs)

[nf-core/fastquorum](https://nf-co.re/fastquorum/1.1.0/) is a bioinformatics pipeline that
implements the [fgbio Best Practices FASTQ to Consensus Pipeline](https://github.com/fulcrumgenomics/fgbio/blob/main/docs/best-practice-consensus-pipeline.md)
to produce consensus reads using unique molecular indexes/barcodes (UMIs).
[nf-core/fastquorum](https://nf-co.re/fastquorum/1.1.0/)
can produce consensus reads from single or multi UMI reads, and even
[Duplex Sequencing](https://en.wikipedia.org/wiki/Duplex_sequencing) reads.

![fastquorum subway diagram](https://raw.githubusercontent.com/nf-core/fastquorum/1.1.0//docs/images/fastquorum_subway.png)

### Analysis Steps

1. Read QC ([FastQC](https://www.bioinformatics.babraham.ac.uk/projects/fastqc/))
2. Fastq to BAM, extracting UMIs ([fgbio FastqToBam](http://fulcrumgenomics.github.io/fgbio/tools/latest/FastqToBam.html))
3. Align ([bwa mem](https://github.com/lh3/bwa)), reformat ([fgbio ZipperBam](http://fulcrumgenomics.github.io/fgbio/tools/latest/ZipperBam.html)), and template-coordinate sort ([samtools sort](http://www.htslib.org/doc/samtools.html))
4. Group reads by UMI ([fgbio GroupReadsByUmi](http://fulcrumgenomics.github.io/fgbio/tools/latest/GroupReadsByUmi.html))
5. Call consensus reads ([fgbio CallDuplexConsensusReads](http://fulcrumgenomics.github.io/fgbio/tools/latest/CallDuplexConsensusReads.html) and [fgbio CollectDuplexSeqMetrics](http://fulcrumgenomics.github.io/fgbio/tools/latest/CollectDuplexSeqMetrics.html) for [Duplex-Sequencing data](https://en.wikipedia.org/wiki/Duplex_sequencing); [fgbio CallMolecularConsensusReads](http://fulcrumgenomics.github.io/fgbio/tools/latest/CallMolecularConsensusReads.html) for non-Duplex-Sequencing data)
6. Align ([bwa mem](https://github.com/lh3/bwa))
7. Filter consensus reads ([fgbio FilterConsensusReads](http://fulcrumgenomics.github.io/fgbio/tools/latest/FilterConsensusReads.html))
8. Present QC ([MultiQC](http://multiqc.info/))

