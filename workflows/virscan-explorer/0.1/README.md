# VirScan Explorer 0.1

Configuration for the `sminot-virscan-explorer` process.

Workflow code: [sminot/virscan-explorer](https://github.com/sminot/virscan-explorer),
branch `main`, entry point `main.nf`.

Merges organism-level scores from one or more VirScan (PhIP-Flow) runs with a sample
metadata table and publishes an interactive Observable Framework site, served by the
portal's Web Viewer from the output dataset.

## Inputs

Runs on the output of the VirScan PhIP-Flow processes, and accepts **more than one**
input dataset, because a cohort is normally sequenced across several VirScan runs.

`preprocess.py` assembles the selected datasets into the workflow's `inputs` parameter
and refuses a set whose peptide library, library version or Z-score threshold differ,
since scores called against different libraries or thresholds are not comparable. Its
pure logic is covered by `test_preprocess.py`, runnable offline with
`python -m unittest discover .`

## Parameters

| Parameter | Required | Meaning |
|---|---|---|
| `metadata` | yes | CSV with one row per sample. Defines the cohort: only listed samples are analysed. |
| `sample_id_column` | yes | Column holding the VirScan sample ID, default `vs_id`. |
| `participant_column` | no | Column identifying the participant, for repeated measures. |
| `virus_annotations` | no | CSV with an `organism` column plus grouping columns. |

## Output

A static site published at the root of the dataset's data directory, so `index.html`
lands where the Web Viewer looks for it, plus the merged tables and a snapshot of the
input metadata under `tables/`.
