
from cirro.helpers.preprocess_dataset import PreprocessDataset

# Instantiate the Cirro dataset object
ds = PreprocessDataset.from_running()

# Write out the sample metadata as a CSV
ds.samplesheet.to_csv("metadata.csv", index=None)

# Log the parameters present
for k, v in ds.params.items():
    ds.logger.info(f"{k}: {v}")
