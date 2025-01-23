#!/usr/bin/env python3

from cirro.helpers.preprocess_dataset import PreprocessDataset
import pandas as pd
from cirro.api.models.s3_path import S3Path
import boto3
import json


def make_manifest(ds: PreprocessDataset) -> pd.DataFrame:
    """Construct a manifest with the paired FASTQ files in the input"""

    ds.logger.info(f"Number of files in dataset: {ds.files.shape[0]:,}")
    ds.logger.info(f"Number of samples in dataset: {ds.samplesheet.shape[0]:,}")

    # Build the manifest
    manifest = (
        ds.files
        .reindex(columns=["sampleIndex", "libraryIndex", "sample", "dataset", "readType", "read", "file"])
        .assign(
            fastq_cname_ix=lambda df: df.apply(
                lambda r: r["read"] + (2 if r.get("readType", "R") == "R" else 0),
                axis=1
            )
        )
        .pivot(
            index=["sampleIndex", "libraryIndex", "sample", "dataset"],
            columns="fastq_cname_ix",
            values="file"
        )
        .rename(columns=lambda i: f"fastq_{int(i)}")
        .sort_index()
        .sort_index(axis=1)
        .reset_index()
        .drop(columns=["sampleIndex", "libraryIndex", "dataset"])
    )

    log_table(ds, "Manifest", manifest)

    # Get the read_structure attribute for each sample (if any exists)
    read_structure = ds.samplesheet.reindex(
        columns=["sample", "read_structure"]
    ).set_index(
        "sample"
    )["read_structure"].dropna()

    # Log the number of samples which have read_structure defined
    if read_structure.shape[0] == 0:
        ds.log("No samples have read_structure defined by the samplesheet")
    else:
        for sample, rs in read_structure.items():
            ds.log(f"Sample: {sample} - Read Structure: {rs}")

    ds.log(f"Any missing read_structures will be populated with {ds.params['read_structure']}")

    # Add that information to the manifest, filling in the form value when missing
    manifest = manifest.assign(
        read_structure=manifest["sample"].apply(
            read_structure.get
        ).fillna(
            ds.params["read_structure"]
        )
    )
    log_table(ds, "Manifest", manifest)

    return manifest


def log_table(ds: PreprocessDataset, title: str, df: pd.DataFrame):
    ds.logger.info(f"{title}:")
    for line in df.to_csv(index=None).split("\n"):
        ds.logger.info(line)


if __name__ == "__main__":

    ds = PreprocessDataset.from_running()

    manifest = make_manifest(ds)

    # Write out the manifest
    manifest.to_csv("manifest.csv", index=None)
    ds.logger.info(f"Wrote out {manifest.shape[0]:,} lines to manifest.csv")
