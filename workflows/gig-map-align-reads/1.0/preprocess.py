
from cirro.helpers.preprocess_dataset import PreprocessDataset

# Instantiate the Cirro dataset object
ds = PreprocessDataset.from_running()

# Filter out any index files that may have been uploaded
ds.files = ds.files.loc[
    ds.files.apply(
        lambda r: r.get('readType', 'R') == 'R',
        axis=1
    )
]

# Make a wide samplesheet
samplesheet = ds.wide_samplesheet(
    index=["sample", "sampleIndex", "dataset"],
    columns="read",
    values="file",
    column_prefix="R"
).reindex(
    columns=["sample", "R1", "R2"]
)
assert samplesheet.shape[0] > 0, "No files detected -- there may be an error with data ingest"

ds.logger.info("Samplesheet:")
ds.logger.info(samplesheet.to_csv(index=None))

# Write out the sample sheet
ds.logger.info(f"Writing out {samplesheet.shape[0]:,} lines to samplesheet.csv")
samplesheet.to_csv(
    "samplesheet.csv",
    index=None
)

# Add it to the params
ds.add_param(
    "samplesheet",
    "samplesheet.csv"
)

# Log the parameters present
for k, v in ds.params.items():
    ds.logger.info(f"{k}: {v}")
