#!/usr/bin/env python3

from cirro.helpers.preprocess_dataset import PreprocessDataset

ds = PreprocessDataset.from_running()

# Check the parameters
assert len(ds.params.get("input", "")) > 0, "Must provide Input file"

msg = "Must provide formula indicating columns to test"
assert len(ds.params.get("formula", "")) > 0, msg

for kw in ["min_abund", "fdr_cutoff"]:
    assert ds.params[kw] >= 0, f"{kw} must be >= 0"
    assert ds.params[kw] < 1, f"{kw} must be < 1"
