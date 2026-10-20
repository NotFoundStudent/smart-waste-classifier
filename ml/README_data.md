# Dataset Versioning and Data Provenance

## Dataset Overview

- Dataset path: data/waste.csv
- Dataset format: CSV
- Original dataset size: 32 rows
- Input features: weight_g, moisture_pct, magnetic
- Target column: category
- Valid categories: plastic, metal, paper, organic
- DVC tracking file: data/waste.csv.dvc
- The raw dataset is versioned by DVC rather than committed directly to Git.

## Data Source

The project uses the local dataset at data/waste.csv. The original source and collection method should be confirmed by the project team.

- v1: documented as 32 rows, with 8 samples per category.
- v2: documented as 64 rows, with 16 samples per category, cleaned and augmented by ml/make_v2_dataset.py.

## Dataset Versions

### Version 1 (v1)

- Git commit: b366261
- Description: documented as 32 rows, with 8 samples per category.

### Version 2 (v2)

- Git commit: d4b329b
- Description: documented as cleaned and augmented to 64 rows, with small Gaussian noise applied to numeric features for synthetic samples.

The version details above should be verified against the actual DVC history.

## DVC and Remote Storage

The project documentation records an Azure DVC remote at azure://dvc/smart-waste-classifier/ named myazure, with local authentication configuration in .dvc/config.local. No credentials should be committed to Git.

Confirm the remote configuration and that v1/v2 can be restored from the DVC remote before relying on these details.

## Reproducibility

ML experiments should record the dataset version or content hash used for each run. See ml/README_experiments.md and ml/PROVENANCE.md.
