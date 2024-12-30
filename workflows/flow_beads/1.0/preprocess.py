#!/usr/bin/env python3

from cirro.helpers.preprocess_dataset import PreprocessDataset

ds = PreprocessDataset.from_running()


def _deduplicate_fcs(fcs_files: str) -> str:
    """
    Deduplicate a comma-separated list of FCS files,
    making sure that the file names are all unique
    (even if some files are in different folders).

    :param fcs_files: Comma-separated list of FCS files.
    :return: Deduplicated comma-separated list of FCS files.
    """
    # This pattern is being used to differentiate the URI from the filename
    seen = set([])
    output = []

    for file in fcs_files.split(","):
        fn = file.split("/")[-1]
        if fn in seen:
            ds.logger.warning(f"Removing duplicate file: {file}")
        else:
            seen.add(fn)
            output.append(file)

    return ",".join(output)


if len(ds.params.get("subset", "")) > 0:
    n = len(ds.params['subset'].split(","))
    ds.logger.info(f"User specified a subset of {n:,} files to analyze")
    ds.add_param(
        "input_fcs",
        _deduplicate_fcs(ds.params["subset"]),
        overwrite=True
    )
else:
    ds.logger.info("No subset specified -- analyzing all files")

    input_fcs = [
        file
        for file in ds.files["file"].tolist()
        if file.endswith(".fcs")
    ]
    ds.logger.info(f"Found {len(input_fcs):,} FCS files to analyze")
    ds.add_param(
        "input_fcs",
        _deduplicate_fcs(",".join(input_fcs))
    )

    input_anndata = [
        file
        for file in ds.files["file"].tolist()
        if file.endswith(".h5ad")
    ]
    if len(input_anndata) > 0:
        ds.logger.info(f"Found {len(input_anndata):,} anndata files to analyze")
        ds.add_param(
            "input_anndata",
            ",".join(input_anndata)
        )
    else:
        ds.logger.info("No anndata files found")

# log
ds.logger.info(ds.params)
