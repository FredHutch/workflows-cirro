#!/usr/bin/env python3

from cirro.helpers.preprocess_dataset import PreprocessDataset

ds = PreprocessDataset.from_running()

ds.logger.info("Files annotated in the dataset:")
ds.logger.info(ds.files.to_csv(index=None))

# There may only be a single file per sample
if ds.files['sample'].value_counts().max() > 1:
    raise Exception("Only one FASTA is allowed per genome")

# Make a simple table with each of the files listed on single row
samplesheet = ds.files.rename(
    columns=dict(
        file="fasta",
        sample="name"
    )
).reindex(
    columns=["name", "fasta"]
)
samplesheet.to_csv(
    "samplesheet.csv",
    index=False
)

ds.logger.info("Samplesheet:")
ds.logger.info(samplesheet.to_csv(index=None))

# log
ds.logger.info(ds.params)