#!/usr/bin/env python3
from cirro.helpers.preprocess_dataset import PreprocessDataset


if __name__ == '__main__':
    ds = PreprocessDataset.from_running()

    # Set the memory based on the number of CPUs
    ds.add_param(
        "memory_gb",
        {
            4: 7,
            16: 30,
            36: 60
        }[
            int(ds.params['cpus'])
        ]
    )

    # Make sure that the options have been set
    if ds.params.get("options") is None:
        ds.add_param("options", "")
