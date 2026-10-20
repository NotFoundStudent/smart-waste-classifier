# Model and Data Provenance

## Dataset

- Path: `data/waste.csv`
- SHA-256: `36ca8a66e6acb46a78cfea256905c5b5f0c20e6483456f5f1460439da622c2a0`
- Dataset size used in the experiments: 32 rows
- Features: `weight_g`, `moisture_pct`, `magnetic`
- Target column: `category`

The hash identifies the dataset file used for the recorded experiments. A DVC version identifier is not asserted in this document.

## Code Revision

Git HEAD SHA recorded by the training script:

`3c2ec0279e8d2a493d782ad9cd1f3111106db1ed`

Note: the training script records the current Git HEAD. If source files have uncommitted modifications, this SHA does not uniquely identify those modified file contents.

## Training Configuration

- Algorithm: Logistic Regression
- Pipeline: StandardScaler followed by Logistic Regression
- Maximum iterations: 1000
- Random state: 42
- Test size: 25%
- Compared C values: 1.0 and 0.1

## MLflow Runs

| C | MLflow Run ID | Accuracy | Weighted F1 |
|---:|---|---:|---:|
| 1.0 | `9e75066194744e4fa30834d894b29f90` | 0.625 | 0.600 |
| 0.1 | `886c9afb12aa4b6e8a249595f9b58e48` | 0.750 | 0.667 |

Each MLflow run records parameters, metrics, provenance tags, and artifacts. Results are preliminary because the dataset and test set are small.
