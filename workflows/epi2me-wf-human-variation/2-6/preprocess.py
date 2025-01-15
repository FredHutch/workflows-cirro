#!/usr/bin/env python3
from cirro.helpers.preprocess_dataset import PreprocessDataset

def setup_genome(ds: PreprocessDataset):

    # Define the map of genome names to files
    igenomes_base = "s3://pubweb-references/igenomes"

    genome_files = {
        'Homo sapiens (GRCh37)': {
            'fasta': f"{igenomes_base}/Homo_sapiens/Ensembl/GRCh37/Sequence/WholeGenomeFasta/genome.fa",
            'bed12': f"{igenomes_base}/Homo_sapiens/Ensembl/GRCh37/Annotation/Genes/genes.bed"
        },
        'Homo sapiens (GRCh38)': {
            'fasta': f"{igenomes_base}/Homo_sapiens/NCBI/GRCh38/Sequence/WholeGenomeFasta/genome.fa",
            'bed12': f"{igenomes_base}/Homo_sapiens/NCBI/GRCh38/Annotation/Genes/genes.bed"
        },
        'Mus musculus (GRCm38)': {
            'fasta': f"{igenomes_base}/Mus_musculus/Ensembl/GRCm38/Sequence/WholeGenomeFasta/genome.fa",
            'bed12': f"{igenomes_base}/Mus_musculus/Ensembl/GRCm38/Annotation/Genes/genes.bed"
        },
        'Arabidopsis thaliana (TAIR10)': {
            'fasta': f"{igenomes_base}/Arabidopsis_thaliana/Ensembl/TAIR10/Sequence/WholeGenomeFasta/genome.fa",
            'bed12': f"{igenomes_base}/Arabidopsis_thaliana/Ensembl/TAIR10/Annotation/Genes/genes.bed"
        },
        'Bacillus subtilis_168 (EB2)': {
            'fasta': f"{igenomes_base}/Bacillus_subtilis_168/Ensembl/EB2/Sequence/WholeGenomeFasta/genome.fa",
            'bed12': f"{igenomes_base}/Bacillus_subtilis_168/Ensembl/EB2/Annotation/Genes/genes.bed"
        },
        'Bos taurus (UMD3).1': {
            'fasta': f"{igenomes_base}/Bos_taurus/Ensembl/UMD3.1/Sequence/WholeGenomeFasta/genome.fa",
            'bed12': f"{igenomes_base}/Bos_taurus/Ensembl/UMD3.1/Annotation/Genes/genes.bed"
        },
        'Caenorhabditis elegans (WBcel235)': {
            'fasta': f"{igenomes_base}/Caenorhabditis_elegans/Ensembl/WBcel235/Sequence/WholeGenomeFasta/genome.fa",
            'bed12': f"{igenomes_base}/Caenorhabditis_elegans/Ensembl/WBcel235/Annotation/Genes/genes.bed"
        },
        'Canis familiaris (CanFam3).1': {
            'fasta': f"{igenomes_base}/Canis_familiaris/Ensembl/CanFam3.1/Sequence/WholeGenomeFasta/genome.fa",
            'bed12': f"{igenomes_base}/Canis_familiaris/Ensembl/CanFam3.1/Annotation/Genes/genes.bed"
        },
        'Danio rerio (GRCz10)': {
            'fasta': f"{igenomes_base}/Danio_rerio/Ensembl/GRCz10/Sequence/WholeGenomeFasta/genome.fa",
            'bed12': f"{igenomes_base}/Danio_rerio/Ensembl/GRCz10/Annotation/Genes/genes.bed"
        },
        'Drosophila melanogaster (BDGP6)': {
            'fasta': f"{igenomes_base}/Drosophila_melanogaster/Ensembl/BDGP6/Sequence/WholeGenomeFasta/genome.fa",
            'bed12': f"{igenomes_base}/Drosophila_melanogaster/Ensembl/BDGP6/Annotation/Genes/genes.bed"
        },
        'Equus caballus (EquCab2)': {
            'fasta': f"{igenomes_base}/Equus_caballus/Ensembl/EquCab2/Sequence/WholeGenomeFasta/genome.fa",
            'bed12': f"{igenomes_base}/Equus_caballus/Ensembl/EquCab2/Annotation/Genes/genes.bed"
        },
        'Escherichia coli_K_12_DH10B (EB1)': {
            'fasta': f"{igenomes_base}/Escherichia_coli_K_12_DH10B/Ensembl/EB1/Sequence/WholeGenomeFasta/genome.fa",
            'bed12': f"{igenomes_base}/Escherichia_coli_K_12_DH10B/Ensembl/EB1/Annotation/Genes/genes.bed"
        },
        'Gallus gallus (Galgal4)': {
            'fasta': f"{igenomes_base}/Gallus_gallus/Ensembl/Galgal4/Sequence/WholeGenomeFasta/genome.fa",
            'bed12': f"{igenomes_base}/Gallus_gallus/Ensembl/Galgal4/Annotation/Genes/genes.bed"
        },
        'Glycine max (Gm01)': {
            'fasta': f"{igenomes_base}/Glycine_max/Ensembl/Gm01/Sequence/WholeGenomeFasta/genome.fa",
            'bed12': f"{igenomes_base}/Glycine_max/Ensembl/Gm01/Annotation/Genes/genes.bed"
        },
        'Macaca mulatta (Mmul_1)': {
            'fasta': f"{igenomes_base}/Macaca_mulatta/Ensembl/Mmul_1/Sequence/WholeGenomeFasta/genome.fa",
            'bed12': f"{igenomes_base}/Macaca_mulatta/Ensembl/Mmul_1/Annotation/Genes/genes.bed"
        },
        'Oryza sativa_japonica (IRGSP)-1.0': {
            'fasta': f"{igenomes_base}/Oryza_sativa_japonica/Ensembl/IRGSP-1.0/Sequence/WholeGenomeFasta/genome.fa",
            'bed12': f"{igenomes_base}/Oryza_sativa_japonica/Ensembl/IRGSP-1.0/Annotation/Genes/genes.bed"
        },
        'Pan troglodytes (CHIMP2).1.4': {
            'fasta': f"{igenomes_base}/Pan_troglodytes/Ensembl/CHIMP2.1.4/Sequence/WholeGenomeFasta/genome.fa",
            'bed12': f"{igenomes_base}/Pan_troglodytes/Ensembl/CHIMP2.1.4/Annotation/Genes/genes.bed"
        },
        'Rattus norvegicus (Rnor_5).0': {
            'fasta': f"{igenomes_base}/Rattus_norvegicus/Ensembl/Rnor_5.0/Sequence/WholeGenomeFasta/genome.fa",
            'bed12': f"{igenomes_base}/Rattus_norvegicus/Ensembl/Rnor_5.0/Annotation/Genes/genes.bed"
        },
        'Rattus norvegicus (Rnor_6).0': {
            'fasta': f"{igenomes_base}/Rattus_norvegicus/Ensembl/Rnor_6.0/Sequence/WholeGenomeFasta/genome.fa",
            'bed12': f"{igenomes_base}/Rattus_norvegicus/Ensembl/Rnor_6.0/Annotation/Genes/genes.bed"
        },
        'Saccharomyces cerevisiae (R64)-1-1': {
            'fasta': f"{igenomes_base}/Saccharomyces_cerevisiae/Ensembl/R64-1-1/Sequence/WholeGenomeFasta/genome.fa",
            'bed12': f"{igenomes_base}/Saccharomyces_cerevisiae/Ensembl/R64-1-1/Annotation/Genes/genes.bed"
        },
        'Schizosaccharomyces pombe (EF2)': {
            'fasta': f"{igenomes_base}/Schizosaccharomyces_pombe/Ensembl/EF2/Sequence/WholeGenomeFasta/genome.fa",
            'bed12': f"{igenomes_base}/Schizosaccharomyces_pombe/Ensembl/EF2/Annotation/Genes/genes.bed"
        },
        'Sorghum bicolor (Sbi1)': {
            'fasta': f"{igenomes_base}/Sorghum_bicolor/Ensembl/Sbi1/Sequence/WholeGenomeFasta/genome.fa",
            'bed12': f"{igenomes_base}/Sorghum_bicolor/Ensembl/Sbi1/Annotation/Genes/genes.bed"
        },
        'Sus scrofa (Sscrofa10).2': {
            'fasta': f"{igenomes_base}/Sus_scrofa/Ensembl/Sscrofa10.2/Sequence/WholeGenomeFasta/genome.fa",
            'bed12': f"{igenomes_base}/Sus_scrofa/Ensembl/Sscrofa10.2/Annotation/Genes/genes.bed"
        },
        'Zea mays (AGPv3)': {
            'fasta': f"{igenomes_base}/Zea_mays/Ensembl/AGPv3/Sequence/WholeGenomeFasta/genome.fa",
            'bed12': f"{igenomes_base}/Zea_mays/Ensembl/AGPv3/Annotation/Genes/genes.bed"
        },
        'Homo sapiens (hg38)': {
            'fasta': f"{igenomes_base}/Homo_sapiens/UCSC/hg38/Sequence/WholeGenomeFasta/genome.fa",
            'bed12': f"{igenomes_base}/Homo_sapiens/UCSC/hg38/Annotation/Genes/genes.bed"
        },
        'Homo sapiens (hg19)': {
            'fasta': f"{igenomes_base}/Homo_sapiens/UCSC/hg19/Sequence/WholeGenomeFasta/genome.fa",
            'bed12': f"{igenomes_base}/Homo_sapiens/UCSC/hg19/Annotation/Genes/genes.bed"
        },
        'Mus musculus (mm10)': {
            'fasta': f"{igenomes_base}/Mus_musculus/UCSC/mm10/Sequence/WholeGenomeFasta/genome.fa",
            'bed12': f"{igenomes_base}/Mus_musculus/UCSC/mm10/Annotation/Genes/genes.bed"
        },
        'Bos taurus (bosTau8)': {
            'fasta': f"{igenomes_base}/Bos_taurus/UCSC/bosTau8/Sequence/WholeGenomeFasta/genome.fa",
            'bed12': f"{igenomes_base}/Bos_taurus/UCSC/bosTau8/Annotation/Genes/genes.bed"
        },
        'Caenorhabditis elegans (ce10)': {
            'fasta': f"{igenomes_base}/Caenorhabditis_elegans/UCSC/ce10/Sequence/WholeGenomeFasta/genome.fa",
            'bed12': f"{igenomes_base}/Caenorhabditis_elegans/UCSC/ce10/Annotation/Genes/genes.bed"
        },
        'Canis familiaris (canFam3)': {
            'fasta': f"{igenomes_base}/Canis_familiaris/UCSC/canFam3/Sequence/WholeGenomeFasta/genome.fa",
            'bed12': f"{igenomes_base}/Canis_familiaris/UCSC/canFam3/Annotation/Genes/genes.bed"
        },
        'Danio rerio (danRer10)': {
            'fasta': f"{igenomes_base}/Danio_rerio/UCSC/danRer10/Sequence/WholeGenomeFasta/genome.fa",
            'bed12': f"{igenomes_base}/Danio_rerio/UCSC/danRer10/Annotation/Genes/genes.bed"
        },
        'Drosophila melanogaster (dm6)': {
            'fasta': f"{igenomes_base}/Drosophila_melanogaster/UCSC/dm6/Sequence/WholeGenomeFasta/genome.fa",
            'bed12': f"{igenomes_base}/Drosophila_melanogaster/UCSC/dm6/Annotation/Genes/genes.bed"
        },
        'Equus caballus (equCab2)': {
            'fasta': f"{igenomes_base}/Equus_caballus/UCSC/equCab2/Sequence/WholeGenomeFasta/genome.fa",
            'bed12': f"{igenomes_base}/Equus_caballus/UCSC/equCab2/Annotation/Genes/genes.bed"
        },
        'Gallus gallus (galGal4)': {
            'fasta': f"{igenomes_base}/Gallus_gallus/UCSC/galGal4/Sequence/WholeGenomeFasta/genome.fa",
            'bed12': f"{igenomes_base}/Gallus_gallus/UCSC/galGal4/Annotation/Genes/genes.bed"
        },
        'Pan troglodytes (panTro4)': {
            'fasta': f"{igenomes_base}/Pan_troglodytes/UCSC/panTro4/Sequence/WholeGenomeFasta/genome.fa",
            'bed12': f"{igenomes_base}/Pan_troglodytes/UCSC/panTro4/Annotation/Genes/genes.bed"
        },
        'Rattus norvegicus (rn6)': {
            'fasta': f"{igenomes_base}/Rattus_norvegicus/UCSC/rn6/Sequence/WholeGenomeFasta/genome.fa",
            'bed12': f"{igenomes_base}/Rattus_norvegicus/UCSC/rn6/Annotation/Genes/genes.bed"
        },
        'Sus scrofa (susScr3)': {
            'fasta': f"{igenomes_base}/Sus_scrofa/UCSC/susScr3/Sequence/WholeGenomeFasta/genome.fa",
            'bed12': f"{igenomes_base}/Sus_scrofa/UCSC/susScr3/Annotation/Genes/genes.bed"
        }
    }

    # Make sure that the user selected a valid genome name
    assert ds.params.get('org') in genome_files, f"ERROR: Invalid genome name '{ds.params.get('org')}'"
    # Add the associated 'fasta' (as 'ref') and 'bed12' (as 'bed') files to the dataset
    ds.add_param('ref', genome_files[ds.params.get('org')]['fasta'])
    ds.add_param('bed', genome_files[ds.params.get('org')]['bed12'])

    # Remove the 'org' param
    ds.remove_param('org')


def setup_cnv(ds: PreprocessDataset):
    # Manage the CNV caller param
    cnv = ds.params.get('cnv')
    if cnv == "Disabled":
        ds.add_param('cnv', False, overwrite=True)
    elif cnv == "Spectre":
        ds.add_param('cnv', True, overwrite=True)
    else:
        assert cnv == "QDNAseq", f"ERROR: Invalid CNV caller '{cnv}'"
        ds.add_param('cnv', True, overwrite=True)
        ds.add_param('use_qdnaseq', True, overwrite=True)


def setup_analysis_modules(ds: PreprocessDataset):

    for kw in ["sv", "snp", "mod", "str"]:
        if ds.params.get(kw, "Disabled") == "Disabled":
            ds.add_param(kw, False, overwrite=True)
        else:
            ds.add_param(kw, True, overwrite=True)


def setup_basecaller_configuration(ds: PreprocessDataset):
    # If the user selected 'autoselect' for override_basecaller_cfg, delete the param
    if ds.params.get('override_basecaller_cfg') == 'autoselect':
        ds.remove_param('override_basecaller_cfg')


if __name__ == '__main__':
    # Load information from the dataset
    ds = PreprocessDataset.from_running()

    setup_genome(ds)
    setup_analysis_modules(ds)
    setup_cnv(ds)
    setup_basecaller_configuration(ds)
