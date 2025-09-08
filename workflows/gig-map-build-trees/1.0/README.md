# Build Trees (gig-map/build_trees)

Build phylogenetic trees for each bin.

For each bin, the sequences for each gene will be built into a multiple sequence alignment
using CLUSTAL Omega.
Those alignments will be combined into an aggregate pairwise distance matrix, and also used
to build a phylogenetic tree using RAxML-NG.


Workflow Engine: Nextflow


Category: Microbial Analysis


Documentation: [https://docs.cirro.bio/pipelines/catalog-microbial-analysis#microbial-pangenome-gig-map](https://docs.cirro.bio/pipelines/catalog-microbial-analysis#microbial-pangenome-gig-map)


Source: [FredHutch/gig-map](FredHutch/gig-map)


Version: `main`


Script: `build_trees.nf`
