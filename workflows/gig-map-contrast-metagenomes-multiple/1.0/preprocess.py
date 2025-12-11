
import json
import os
from cirro.helpers.preprocess_dataset import PreprocessDataset
from subprocess import call


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


def main():

    # Instantiate the Cirro dataset object
    ds = PreprocessDataset.from_running()

    # Get the gene_bins.csv path by inspecting the input dataset
    gene_bins = find_pangenome_file(ds, "/data/bin_pangenome/gene_bins.csv")
    ds.add_param("gene_bins", gene_bins)
    # Do the same thing for the centroids FAA
    centroids_faa = find_pangenome_file(ds, "/data/gene_catalog/centroids.faa.gz")
    ds.add_param("centroids_faa", centroids_faa)

    # Log the parameters present
    for k, v in ds.params.items():
        ds.logger.info(f"{k}: {v}")


if __name__ == "__main__":
    main()
