#!/usr/bin/env python3

from cirro.helpers.preprocess_dataset import PreprocessDataset
import pandas as pd

ds = PreprocessDataset.from_running()


def log_table(title: str, df: pd.DataFrame, **kwargs):
    ds.logger.info(title)
    msg = "No rows found in table -- stopping"
    assert df.shape[0] > 0, msg
    for line in df.to_csv(**kwargs).split("\n"):
        ds.logger.info(line)


def make_samplesheet() -> pd.DataFrame:

    log_table("File Table", ds.files)
    log_table("Sample metadata", ds.samplesheet)

    samplesheet = (
        ds.files
        .merge(
            ds.samplesheet,
            right_on="sample",
            left_on="sample"
        )
        .set_index("sample")
    )

    # Drop the sampleIndex column if it's present
    if "sampleIndex" in samplesheet.columns.values:
        samplesheet = samplesheet.drop(columns=["sampleIndex"])

    log_table("Merged", samplesheet)

    ds.add_param("samplesheet", "samplesheet.csv")
    samplesheet.to_csv("samplesheet.csv")


def main():
    # Get the input data
    make_samplesheet()

    msg = "Must provide formula indicating columns to test"
    assert len(ds.params.get("formula", "")) > 0, msg

    for kw in ["min_abund", "fdr_cutoff"]:
        assert ds.params[kw] >= 0, f"{kw} must be >= 0"
        assert ds.params[kw] < 1, f"{kw} must be < 1"


if __name__ == "__main__":
    main()
