#!/usr/bin/env python3

from cirro.helpers.preprocess_dataset import PreprocessDataset
import json
import yaml

# Read the information set up for this workflow
ds = PreprocessDataset.from_running()

# Log the parameters provided by the user
ds.logger.info(json.dumps(ds.params, indent=4))

#####################
# PARAMETER NESTING #
#####################

# The form shown to the user was not constructed with the full
# degree of nesting which is needed in the final output.
# The reason for making the flattened form is so that the
# rendered form is more visually readable.
# To make sure that the workflow runs well, those params should
# be re-nested.


def renest(obj):
    if not isinstance(obj, dict):
        return obj

    to_remove = []
    to_add = dict()
    for kw, val in obj.items():
        if "." in kw:
            start, end = kw.split(".", 1)
            if start not in to_add:
                to_add[start] = dict()
            to_add[start][end] = val
            to_remove.append(kw)
    obj = {
        kw: val
        for kw, val in obj.items()
        if kw not in to_remove
    }
    for kw, val in to_add.items():
        obj[kw] = renest(val)

    return obj


##########################
# WORKFLOW CONFIGURATION #
##########################

# Point to the config element as a single dict
config = renest(ds.params["config"])
ds.remove_param("config")

# Add the information on the inputs
# Note that the filepaths set up here correspond to the
# location of those files inside the Nextflow task used
# to run nextstrain
config["inputs"] = [
    {
        "name": "local-data",
        "sequences": "data/custom.sequences.fasta",
        "metadata": "data/custom.metadata.tsv"
    }
]

# Log as both JSON and YAML
ds.logger.info("Workflow Config (JSON):")
ds.logger.info(json.dumps(config, indent=4))

ds.logger.info("Workflow Config (YAML):")
ds.logger.info(yaml.dump(config))

# Write out as YAML
with open("configfile.yaml", "w") as handle:
    yaml.dump(config, handle)

# Add that file as a param for the workflow
ds.add_param("configfile", "configfile.yaml")

#########################
# AUSPICE CONFIGURATION #
#########################

# Parse the auspice configuration selections
auspice = renest(ds.params["auspice"])
ds.remove_param("auspice")

# Add in the default elements which were not presented in the form
auspice["build_url"] = f"https://github.com/nextstrain/{ds.params['workflow']}"
auspice["colorings"] = [
    {
        "key": "emerging_lineage",
        "title": "Emerging Lineage",
        "type": "categorical"
    },
    {
        "key": "immune_escape",
        "title": "Immune Escape vs BA.2",
        "type": "continuous"
    },
    {
        "key": "ace2_binding",
        "title": "ACE2 binding vs BA.2",
        "type": "continuous"
    },
    {
        "key": "pango_lineage",
        "title": "PANGO Lineage",
        "type": "categorical"
    },
    {
        "key": "GISAID_clade",
        "title": "GISAID Clade",
        "type": "categorical"
    },
    {
        "key": "S1_mutations",
        "title": "S1 mutations",
        "type": "continuous"
    },
    {
        "key": "logistic_growth",
        "title": "Logistic growth",
        "type": "continuous"
    },
    {
        "key": "current_frequency",
        "title": "Current frequency",
        "type": "continuous"
    },
    {
        "key": "mutational_fitness",
        "title": "Mutational fitness",
        "type": "continuous"
    },
    {
        "key": "location",
        "title": "Location",
        "type": "categorical"
    },
    {
        "key": "division",
        "title": "Admin Division",
        "type": "categorical"
    },
    {
        "key": "country",
        "title": "Country",
        "type": "categorical"
    },
    {
        "key": "region",
        "title": "Region",
        "type": "categorical"
    },
    {
        "key": "host",
        "title": "Host",
        "type": "categorical"
    },
    {
        "key": "age",
        "title": "Age",
        "type": "continuous"
    },
    {
        "key": "sex",
        "title": "Sex",
        "type": "categorical"
    },
    {
        "key": "author",
        "title": "Authors",
        "type": "categorical"
    },
    {
        "key": "originating_lab",
        "title": "Originating Lab",
        "type": "categorical"
    },
    {
        "key": "submitting_lab",
        "title": "Submitting Lab",
        "type": "categorical"
    },
    {
        "key": "recency",
        "title": "Submission Date",
        "type": "categorical"
    },
    {
        "key": "gisaid_epi_isl",
        "type": "categorical"
    },
    {
        "key": "genbank_accession",
        "type": "categorical"
    },
    {
        "key": "epiweek",
        "title": "Epiweek (CDC)",
        "type": "continuous"
    },
    {
        "key": "QC_overall_score",
        "title": "Nextclade QC score",
        "type": "continuous"
    },
    {
        "key": "QC_overall_status",
        "title": "Nextclade QC status",
        "type": "categorical"
    },
    {
        "key": "reversion_mutations",
        "title": "Reversion mutations",
        "type": "continuous"
    },
    {
        "key": "potential_contaminants",
        "title": "Potential contaminants",
        "type": "continuous"
    },
    {
        "key": "rare_mutations",
        "title": "Rare mutations",
        "type": "continuous"
    }
]

# Write to JSON
auspice_json = "auspice_config.json"
with open(auspice_json, "w") as handle:
    json.dump(auspice, handle, indent=4)

# Point the workflow to that file
ds.add_param("auspice", auspice_json, overwrite=True)

################
# READY TO RUN #
################

# Log the parameters in the state immediately prior to running
ds.logger.info(json.dumps(ds.params, indent=4))
