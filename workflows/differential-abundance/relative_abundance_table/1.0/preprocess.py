#!/usr/bin/env python3

from cirro.helpers.preprocess_dataset import PreprocessDataset

ds = PreprocessDataset.from_running()


def main():

    msg = "Must provide formula indicating columns to test"
    assert len(ds.params.get("formula", "")) > 0, msg

    for kw in ["min_abund", "fdr_cutoff"]:
        assert ds.params[kw] >= 0, f"{kw} must be >= 0"
        assert ds.params[kw] < 1, f"{kw} must be < 1"


if __name__ == "__main__":
    main()
