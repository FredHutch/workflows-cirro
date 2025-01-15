#!/usr/bin/env python3
from cirro.helpers.preprocess_dataset import PreprocessDataset

def setup_cnv(ds: PreprocessDataset):
    # Manage the CNV caller param
    cnv = ds.params.get('cnv')
    if cnv == "Disabled":
        ds.add_param('cnv', False, overwrite=True)
    elif cnv == "Spectre":
        ds.add_param('cnv', True, overwrite=True)
    else:
        assert cnv == "QDNAseq", f"ERROR: Invalid CNV caller '{cnv}'"
        ds.add_param('cnv', True, overwrite=True)
        ds.add_param('use_qdnaseq', True, overwrite=True)


def setup_analysis_modules(ds: PreprocessDataset):

    for kw in ["sv", "snp", "mod", "str"]:
        if ds.params.get(kw, "Disabled") == "Disabled":
            ds.add_param(kw, False, overwrite=True)
        else:
            ds.add_param(kw, True, overwrite=True)


def setup_basecaller_configuration(ds: PreprocessDataset):
    # If the user selected 'autoselect' for override_basecaller_cfg, delete the param
    if ds.params.get('override_basecaller_cfg') == 'autoselect':
        ds.remove_param('override_basecaller_cfg')


if __name__ == '__main__':
    # Load information from the dataset
    ds = PreprocessDataset.from_running()

    setup_analysis_modules(ds)
    setup_cnv(ds)
    setup_basecaller_configuration(ds)
