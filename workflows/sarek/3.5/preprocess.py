#!/usr/bin/env python3

from cirro.helpers.preprocess_dataset import PreprocessDataset
import pandas as pd


def make_manifest(ds: PreprocessDataset) -> pd.DataFrame:

    # Filter out any index files that may have been uploaded
    ds.files = ds.files.loc[
        ds.files.apply(
            lambda r: r.get('readType', 'R') == 'R',
            axis=1
        )
    ]

    # Make a wide manifest
    manifest = ds.wide_samplesheet(
        index=["sampleIndex", "sample", "lane", "dataset"],
        columns="read",
        values="file",
        column_prefix="fastq_"
    )
    assert manifest.shape[0] > 0, "No files detected -- there may be an error with data ingest"

    # append metadata to file paths
    samples = ds.samplesheet.set_index("sample")
    manifest: pd.DataFrame = manifest.assign(
        **{k: manifest["sample"].apply(v.get) for k, v in samples.items()}
    )
    ordering = ['patient', 'sex', 'status', 'sample', 'lane', 'fastq_1', 'fastq_2']
    manifest = manifest.reindex(columns=ordering)

    # Overwrite the 'lane' column to provide a unique value per-row
    # This is necessary to account for datasets which merge multiple flowcells
    manifest = manifest.assign(lane=[
        str(i+1)
        for i in range(manifest.shape[0])
    ])

    # Set the default value for 'sex' to be NA
    manifest = manifest.assign(
        sex=manifest['sex'].fillna('NA')
    )

    # Transform status values "Normal" -> 0 and "Tumor" -> 1
    manifest = manifest.replace(
        to_replace=dict(
            status=dict(
                normal=0,
                Normal=0,
                tumor=1,
                Tumor=1
            )
        )
    )

    # Set the default status to 0
    manifest = manifest.assign(
        status=manifest["status"].fillna(0).apply(int)
    )

    # Set the default "patient" attribute as the sample
    manifest = manifest.assign(
        patient=manifest["patient"].fillna(manifest["sample"])
    )

    return manifest


if __name__ == "__main__":

    # Load the information for this dataset
    ds = PreprocessDataset.from_running()

    # Make the samplesheet
    manifest = make_manifest(ds)

    # Log the manifest
    ds.logger.info(manifest.to_csv(index=None))

    # Write manifest
    manifest.to_csv("manifest.csv", index=None)

    # JSON parameters !! revert after fix
    params = ds.params

    tools = params.get('tools')
    assert tools is not None, "ERROR: You must select a variant calling tool."

    # Annotation tool is allowed to be empty, init empty list if it is
    # not 100% sure of annotation tool behavior if neither are selected i.e empty
    annotation_tool = params.get('annotation_tool') or []

    # Combine the two
    tools = ','.join(map(str, tools + annotation_tool))

    ds.add_param('tools', tools, overwrite=True)

    # if user does not select VEP/snpEff then annotation tool param does not exist.
    # script sets it as empty list, use this to toggle deleting the param to avoid error.
    if len(annotation_tool) != 0:
        ds.remove_param('annotation_tool')

    # construct logic for dbNSFP & SpliceAI
    # note reference genome selected
    # if true, construct the appropriate parameters as file paths. 
    dbnsfp_param = params.get('vep_dbnsfp') # true or null 
    spliceai = params.get('vep_spliceai') # true or null 
    database = {'GATK.GRCh37': ['GRCh37', 'hg19'],
                'GATK.GRCh38': ['GRCh38', 'hg38']}

    genome = params.get('genome')
    # dbNSFP
    if dbnsfp_param:
        dbnsfp = f"s3://pubweb-references/VEP/{database[genome][0]}/dbNSFP4.2a_{database[genome][0].lower()}.gz"
        dbnsfp_tbi = f"s3://pubweb-references/VEP/{database[genome][0]}/dbNSFP4.2a_{database[genome][0].lower()}.gz.tbi"
        ds.add_param('dbnsfp', dbnsfp, overwrite=True)
        ds.add_param('dbnsfp_tbi', dbnsfp_tbi, overwrite=True)
        ds.add_param('dbnsfp_consequence', 'ALL', overwrite=True)

    # Splice AI
    if spliceai:
        spliceai_snv = f"s3://pubweb-references/VEP/{database[genome][0]}/spliceai_scores.raw.snv.{database[genome][1]}.vcf.gz"
        spliceai_snv_tbi = f"s3://pubweb-references/VEP/{database[genome][0]}/spliceai_scores.raw.snv.{database[genome][1]}.vcf.gz.tbi"
        spliceai_indel = f"s3://pubweb-references/VEP/{database[genome][0]}/spliceai_scores.raw.indel.{database[genome][1]}.vcf.gz"
        spliceai_indel_tbi = f"s3://pubweb-references/VEP/{database[genome][0]}/spliceai_scores.raw.indel.{database[genome][1]}.vcf.gz.tbi"
        ds.add_param('spliceai_snv', spliceai_snv, overwrite=True)
        ds.add_param('spliceai_snv_tbi', spliceai_snv_tbi, overwrite=True)
        ds.add_param('spliceai_indel', spliceai_indel, overwrite=True)
        ds.add_param('spliceai_indel_tbi', spliceai_indel_tbi, overwrite=True)

    # PON handling

    if params.get('analysis_type') == 'Somatic Variant Calling':
        if genome == 'GATK.GRCh37':
            pon = "s3://pubweb-references/igenomes/Homo_sapiens/GATK/GRCh37/Annotation/GATKBundle/Mutect2-WGS-panel-b37.vcf.gz"
            pon_tbi = "s3://pubweb-references/igenomes/Homo_sapiens/GATK/GRCh37/Annotation/GATKBundle/Mutect2-WGS-panel-b37.vcf.gz.tbi"
            ds.add_param('pon', pon, overwrite=True)
            ds.add_param('pon_tbi', pon_tbi, overwrite=True)
        if genome == "GATK.GRCh38":
            pon = "s3://pubweb-references/igenomes/Homo_sapiens/GATK/GRCh38/Annotation/GATKBundle/1000g_pon.hg38.vcf.gz"
            pon_tbi = "s3://pubweb-references/igenomes/Homo_sapiens/GATK/GRCh38/Annotation/GATKBundle/1000g_pon.hg38.vcf.gz.tbi"
            ds.add_param('pon', pon, overwrite=True)
            ds.add_param('pon_tbi', pon_tbi, overwrite=True)    

    ds.remove_param('analysis_type')

    # If an intervals file was not selected, use --no_intervals
    if not ds.params.get("intervals"):
        ds.add_param("no_intervals", True)

    # If the user selected to save alignments in BAM format, set the flag
    if ds.params.get("alignment_format", "CRAM") == "BAM":
        ds.add_param("save_output_as_bam", True)
    ds.remove_param("alignment_format", force=True)

    # log all params
    ds.logger.info(ds.params)
