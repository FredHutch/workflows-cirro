from cirro.helpers.preprocess_dataset import PreprocessDataset
import pandas as pd


def log_table(msg: str, table: pd.DataFrame):
    """Print a message and a table to the Cirro logger."""
    ds.logger.info(msg)
    for line in table.to_csv(index=None).split("\n"):
        ds.logger.info(line)


# If any of the following suffixes are present in the dataset name,
# they will be removed from the name of the dataset
def remove_suffixes(name: str):
    for suffix in [
        " - Quantitative Mass Spectrometry - DDA-LFQ (nf-core/quantms)"
    ]:
        if name.endswith(suffix):
            name = name[: -len(suffix)]
    return name


def make_samplesheet(ds: PreprocessDataset):

    # Format the table of inputs to include:
    # - file: the input file to analyze
    # - id: the unique name of the dataset
    # - name: the name of the dataset provided by the user
    inputs = pd.DataFrame([
        {
            "file": ds_in["s3"] + "/data/proteomicslfq/input.sdrf_openms_design_openms.mzTab",
            "id": ds_in["id"], # GUID
            "sample": remove_suffixes(ds_in["name"]) # Human readable name
        }
        for ds_in in ds.metadata["inputs"]
        if ds_in["processId"] != "hutch-quantms-qc-1-0"
    ])

    log_table("Dataset Inputs:", inputs)

    # Make a samplesheet which merges files with sample metadata
    samplesheet = ds.files.merge(ds.samplesheet, on="sample")

    # Map the dataset GUIDs to the comment field
    comments = (
        samplesheet
        .reindex(columns=['dataset', 'comment'])
        .dropna()
        .groupby("dataset")
        .head(1)
        .set_index("dataset")
        ["comment"]
    )

    if comments.shape[0] > 0:
        ds.logger.info("Dataset comments:")
        for line in comments.to_frame().to_csv().split("\n"):
            ds.logger.info(line)
        inputs = inputs.assign(
            comment=inputs["id"].map(comments)
        )
    else:
        ds.logger.info("No dataset comments available")

    msg = "Dataset names are not unique"
    assert inputs["sample"].nunique() == inputs.shape[0], msg

    # Log the updated table of inputs
    log_table("Dataset IDs -> names:", inputs)

    # Save the table
    inputs.to_csv("samplesheet.csv", index=False)

    # Add the param
    ds.add_param("samplesheet", "samplesheet.csv")


def add_summary_csv(ds: PreprocessDataset):

    # Get any inputs which are QC summary results
    summary_csv = [
        ds_in["s3"] + "/data/summary.csv"
        for ds_in in ds.metadata["inputs"]
        if ds_in["processId"] == "hutch-quantms-qc-1-0"
    ]

    # If there are no files, stop
    if len(summary_csv) == 0:
        return

    # If there is >=1 file, add them all to the dataset
    ds.add_param("summary_csv", ",".join(summary_csv))


if __name__ == "__main__":

    # Instantiate the Cirro dataset object
    ds = PreprocessDataset.from_running()

    # Make the samplesheet
    make_samplesheet(ds)

    # Add any previous set of QC summary metrics, if selected
    add_summary_csv(ds)
