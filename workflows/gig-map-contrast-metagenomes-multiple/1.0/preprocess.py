
import json
import os
from cirro.helpers.preprocess_dataset import PreprocessDataset
from subprocess import call

import pandas as pd


def find_pangenome_files(ds: PreprocessDataset, data_path: str) -> str:
    """For each of the input datasets, run the find_pangenome_file function and return a list of those paths."""

    files = [
        find_pangenome_file(PreprocessDataset.from_path(input_info["s3"]), data_path)
        for input_info in ds.metadata['inputs']
    ]

    # Make sure that all of the files are the same
    assert len(set(files)) == 1, f"All input datasets should have the same pangenome file: {data_path}"

    return files[0]


def find_pangenome_file(ds: PreprocessDataset, data_path: str) -> str:
    # Get the input dataset
    input = ds.metadata['inputs'][0]

    # If the input dataset is annotated with the pangenome used to create it
    if "params" in input and "inputs" in input["params"] and "pangenome" in input["params"]["inputs"]:
        return input["params"]["inputs"]["pangenome"] + data_path

    # If the dataset was uploaded directly
    else:
        # There should be a file present called "pangenome_info.json"
        print("Downloading pangenome info")
        call(["aws", "s3", "cp", input["s3"] + "/data/pangenome_info.json", "./"])
        assert os.path.exists("pangenome_info.json")
        pangenome_info = json.load(open("pangenome_info.json"))

        # Construct the path to the gene bins that are referenced
        s3_base = ds.metadata['dataset']['s3'].rsplit("/", 1)[0]
        return f"{s3_base}/{pangenome_info['uuid']}{data_path}"


def get_read_alignments_file(input_info: dict) -> str:
    # Get the PreprocessDataset object for the input dataset
    ds = PreprocessDataset.from_path(input_info["s3"])

    # Use the dataPath for the first input element
    return ds.metadata['inputs'][0]['dataPath'] + "/read_alignments.csv.gz"


def combine_read_alignments(ds: PreprocessDataset):
    """
    For each of the input datasets, read the CSV from input['dataPath']/read_alignments.csv.gz and concatenate them into a single CSV file.
    Save that file to read_ailgnments.csv.gz, and add that as the `read_alignments` parameter to the dataset.
    """
    # Read in the read alignments from each of the input datasets
    read_alignments_files = [
        get_read_alignments_file(input_info)
        for input_info in ds.metadata['inputs']
    ]

    # Download and concatenate the read alignments using pandas
    combined_read_alignments = []
    for read_alignments_file in read_alignments_files:
        ds.logger.info(f"Reading in read alignments from {read_alignments_file}")
        combined_read_alignments.append(pd.read_csv(read_alignments_file))

    # Write out the combined read alignments
    combined_df: pd.DataFrame = pd.concat(combined_read_alignments)
    combined_df.to_csv("read_alignments.csv.gz", index=False)

    # Add the combined read alignments to the dataset parameters
    ds.add_param("read_alignments", "read_alignments.csv.gz", overwrite=True)


def combine_metadata(ds: PreprocessDataset):
    """
    For each of the input datasets, read the CSV from input['dataPath']/association/metadata.csv and concatenate them into a single CSV file.
    For each one, add the f"{ds.params['batch_prefix']}{input_ix}" column as appropriate.
    Write out the combined metadata to "metadata.csv" and add that to the dataset parameters.
    """

    # Read in the metadata from each of the input datasets
    metadata_files = [
        ds.metadata['inputs'][ix]['dataPath'] + "/association/metadata.csv"
        for ix in range(len(ds.metadata['inputs']))
    ]

    # Download and concatenate the metadata files using pandas
    combined_metadata = []
    for ix, metadata_file in enumerate(metadata_files):
        ds.logger.info(f"Reading in metadata from {metadata_file}")
        df = pd.read_csv(metadata_file)
        if ix > 0:
            cname = ds.params['batch_prefix'] + str(ix)
            df[cname] = 1
            # Add the column to the formula as well
            ds.add_param("formula", f"{ds.params['formula']} + {cname}", overwrite=True)
        combined_metadata.append(df)

    # Write out the combined metadata
    combined_df: pd.DataFrame = pd.concat(combined_metadata)
    # Fill in 0s for the other batches
    combined_df = combined_df.assign(
        **{
            ds.params['batch_prefix'] + str(ix): lambda d: d[ds.params['batch_prefix'] + str(ix)].fillna(0).astype(int)
            for ix in range(1, len(metadata_files))
        }
    )
    combined_df.to_csv("metadata.csv", index=False)

    # Add the combined metadata to the dataset parameters
    ds.add_param("metadata", "metadata.csv", overwrite=True)


def main():

    # Instantiate the Cirro dataset object
    ds = PreprocessDataset.from_running()

    # Get the pangenome used for each of the different analyses (each of which is a contrast_metagenomes.nf run)
    gene_bins = find_pangenome_files(ds, "/data/bin_pangenome/gene_bins.csv")
    ds.add_param("gene_bins", gene_bins)
    # Do the same thing for the centroids FAA
    centroids_faa = find_pangenome_files(ds, "/data/gene_catalog/centroids.faa.gz")
    ds.add_param("centroids_faa", centroids_faa)

    # Combine the metadata from all of the inputs
    combine_metadata(ds)

    # Combine the read alignments from all of the inputs
    combine_read_alignments(ds)

    # Log the parameters present
    for k, v in ds.params.items():
        ds.logger.info(f"{k}: {v}")


if __name__ == "__main__":
    main()
