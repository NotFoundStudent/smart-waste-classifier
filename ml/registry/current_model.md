# Current Model Record

## Status

Selected comparison candidate — not yet validated as production-ready.

## Model

- Algorithm: Logistic Regression
- Pipeline: StandardScaler + Logistic Regression
- Selected C value: 0.1
- Maximum iterations: 1000
- Random state: 42

## Evaluation

- Accuracy: 0.750
- Weighted F1: 0.667
- Test samples: 8
- Dataset rows: 32
- Dataset SHA-256: 36ca8a66e6acb46a78cfea256905c5b5f0c20e6483456f5f1460439da622c2a0

The C=0.1 run scored higher than the C=1.0 run on the current test split. Because the dataset is small and paper classification performed poorly, the result should be treated as preliminary rather than proof of production readiness.

## Per-Class Evaluation

| Category | Precision | Recall | F1 | Support |
|---|---:|---:|---:|---:|
| Metal | 1.000 | 1.000 | 1.000 | 2 |
| Organic | 1.000 | 1.000 | 1.000 | 2 |
| Paper | 0.000 | 0.000 | 0.000 | 2 |
| Plastic | 0.500 | 1.000 | 0.667 | 2 |

The test set contains only 8 samples (2 per category). Paper was not correctly classified in this evaluation, so this model remains a comparison candidate, not a production-ready model.

## MLflow Reference

- Experiment name: baseline
- Run ID: 886c9afb12aa4b6e8a249595f9b58e48
- Recorded Git HEAD SHA: 3c2ec0279e8d2a493d782ad9cd1f3111106db1ed

## Local Artifacts

- Model: models/waste_model.joblib
- Metrics: models/metrics.json

These local files are overwritten by subsequent training runs. Use the referenced MLflow run to access that run's recorded artifacts.
