#!/usr/bin/env python3

from cirro.helpers.preprocess_dataset import PreprocessDataset

ds = PreprocessDataset.from_running()

# Make sure that >= 1 sample is present
assert ds.files.shape[0] > 0, "No input data is present"

# Make sure that the sample IDs are unique
msg = "Sample IDs are not unique"
assert ds.files["sample"].nunique() == ds.files.shape[0], msg

ds.files.to_csv("input.csv", index=False)
