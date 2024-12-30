# Fred Hutch Workflows - Cirro
Collection of Fred Hutch-developed workflow configurations for execution via Cirro

Workflow languages like [WDL](https://openwdl.org), [Nextflow](https://nextflow.io),
and [Snakemake](https://snakemake.readthedocs.io) can be used to automate batch
analysis of datasets.
They can help with:

- Organizing a collection of interconnected analysis steps
- Efficiently utilizing high-performance computing resources
- Granularly controlling the dependencies needed for individual tools
- Sharing with collaborators across institutions

One of the systems used at Fred Hutch data management and analysis is the
[Cirro Data Platform](https://fredhutch.cirro.bio).
This repository contains the Cirro configurations for a collection of workflows
developed by Fred Hutch researchers.
These configurations are used to present a graphical interface for each workflow
so that it can be run via the Cirro web interface.

## Adding Workflows

The components of each workflow configuration are:

- Interactive form for the user to provide inputs (e.g. selecting a reference genome)
- Workflow input setup file, which references items from the form
- (optional) Pre-processing script used for any more complex logic needed to format workflow inputs
- (optional) Computational configuration passed to the workflow executor
- (optional) Output file configuration used for web-native visualizations

For more information, read [the Cirro documentation on configuring workflows](https://docs.cirro.bio/pipelines/adding-pipelines/).

To contribute a new workflow to this repository, simply make a fork and open a pull request.
