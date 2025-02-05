#!/usr/bin/env python3

from cirro.helpers.preprocess_dataset import PreprocessDataset

# Import information about the workflow that was collected from the user,
# this includes the parameters selected from the form, as well as the input
# files from the dataset(s) that were selected
ds = PreprocessDataset.from_running()

# Construct a input sample sheet and save it to "input.csv"
input = (
    ds.files
    .reindex(columns=["sample", "file"])
    .rename(columns=dict(file="filename"))
    .assign(alleles=(
        ds.params["alleles"]
        if ds.params.get("alleles_csv") is None
        else ds.params["alleles_csv"]
    ))
    .assign(mhc_class=ds.params["mhc_class"])
)
# Log the content of the sample sheet
ds.logger.info("Sample Sheet:")
for line in input.to_csv(index=None).split("\n"):
    ds.logger.info(line)
input.to_csv("input.csv", index=None)

ds.remove_param("alleles", force=True)
ds.remove_param("alleles_csv", force=True)
ds.remove_param("mhc_class", force=True)
