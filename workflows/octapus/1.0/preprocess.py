#!/usr/bin/env python3

import re
from cirro.helpers.preprocess_dataset import PreprocessDataset

ds = PreprocessDataset.from_running()

# Format the sample sheet
(
    ds
    .files
    .rename(
        columns=dict(
            sample="#Organism Name",
            file="uri"
        )
    )
    .assign(
        **{"GenBank FTP": ""}
    )
    .to_csv("genomes.csv")
)

ds.add_param(
    "genomes",
    "genomes.csv"
)
