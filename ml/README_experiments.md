# MLflow Experiment Report

## 1. Objective

Compare two Logistic Regression configurations using the same waste dataset and evaluation setup.

## 2. Environment and Dataset

- Dataset: `data/waste.csv`
- Dataset version: Current local dataset; no DVC version is claimed here.
- Dataset rows: 32
- Training samples: 24
- Test samples: 8
- Features: `weight_g`, `moisture_pct`, `magnetic`
- Target: `category`
- Model pipeline: `StandardScaler` + `LogisticRegression`
- Maximum iterations: 1000
- Random state: 42
- Test size: 25%

Dataset SHA-256:

`36ca8a66e6acb46a78cfea256905c5b5f0c20e6483456f5f1460439da622c2a0`

## 3. Experiment Results

Both runs used the same dataset and evaluation setup. The Logistic Regression regularization parameter C was changed.

| Experiment | C | Accuracy | Weighted F1 | MLflow Run ID |
|---|---:|---:|---:|---|
| Baseline | 1.0 | 0.625 | 0.600 | `9e75066194744e4fa30834d894b29f90` |
| Baseline comparison | 0.1 | 0.750 | 0.667 | `886c9afb12aa4b6e8a249595f9b58e48` |

## 4. Analysis

On this test split, C=0.1 achieved higher accuracy and weighted F1 than C=1.0.

The test set contains only 8 samples, so these results are preliminary. They do not establish that C=0.1 will perform better on unseen data in general.

The classification report for the C=0.1 run showed an F1 score of 0.00 for paper, 0.67 for plastic, and 1.00 for metal and organic. Paper classification remains an important weakness.

## 5. Tracking and Artifacts

The training script logs parameters, metrics, Git HEAD SHA, dataset hash, the trained model, and metrics JSON to MLflow.

MLflow Run IDs:
- C=1.0: `9e75066194744e4fa30834d894b29f90`
- C=0.1: `886c9afb12aa4b6e8a249595f9b58e48`

Local output files are saved under `models/`. MLflow also stores artifacts for each individual run.

## 6. Model Selection

C=0.1 is the current comparison candidate because it performed better on this particular test split. Further evaluation with more data is needed before claiming it is production-ready.
