import argparse
import hashlib
import json
import subprocess
from pathlib import Path

import joblib
import mlflow
import mlflow.sklearn
from data_pipeline import load_dataset, split_features_and_labels
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, f1_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = PROJECT_ROOT / "models" / "waste_model.joblib"
METRICS_PATH = PROJECT_ROOT / "models" / "metrics.json"
DATA_PATH = PROJECT_ROOT / "data" / "waste.csv"


def get_git_sha():
    """Return the current Git commit SHA, or a clear fallback."""
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            cwd=PROJECT_ROOT,
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "unknown"


def get_dataset_hash():
    """Identify the exact local dataset file used for training."""
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Dataset not found: {DATA_PATH}")

    digest = hashlib.sha256(DATA_PATH.read_bytes()).hexdigest()
    return digest


def train_model(experiment_name="smart-waste-classifier", c_value=1.0):
    df = load_dataset()
    X, y = split_features_and_labels(df)

    dataset_hash = get_dataset_hash()
    git_sha = get_git_sha()

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.25,
        random_state=42,
        stratify=y,
    )

    model = Pipeline(
        [
            ("scaler", StandardScaler()),
            (
                "classifier",
                LogisticRegression(
                    C=c_value,
                    max_iter=1000,
                    random_state=42,
                ),
            ),
        ]
    )

    mlflow.set_experiment(experiment_name)

    with mlflow.start_run(run_name=f"logistic-regression-C-{c_value}"):
        mlflow.log_params(
            {
                "model_type": "LogisticRegression",
                "C": c_value,
                "max_iter": 2000,
                "test_size": 0.7,
                "random_state": 89,
                "scaler": "StandardScaler",
                "dataset_rows": len(df),
                "train_samples": len(y_train),
                "test_samples": len(y_test),
            }
        )

        mlflow.set_tags(
            {
                "git_commit_sha": git_sha,
                "dataset_sha256": dataset_hash,
                "dataset_version": f"sha256:{dataset_hash}",
            }
        )

        model.fit(X_train, y_train)
        predictions = model.predict(X_test)

        accuracy = accuracy_score(y_test, predictions)
        weighted_f1 = f1_score(
            y_test,
            predictions,
            average="weighted",
            zero_division=0,
        )
        report = classification_report(
            y_test,
            predictions,
            output_dict=True,
            zero_division=0,
        )

        MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(model, MODEL_PATH)

        metrics = {
            "accuracy": accuracy,
            "weighted_f1": weighted_f1,
            "test_samples": len(y_test),
            "classification_report": report,
            "git_commit_sha": git_sha,
            "dataset_sha256": dataset_hash,
            "experiment_name": experiment_name,
            "C": c_value,
        }

        METRICS_PATH.write_text(
            json.dumps(metrics, indent=2),
            encoding="utf-8",
        )

        mlflow.log_metric("accuracy", accuracy)
        mlflow.log_metric("weighted_f1", weighted_f1)
        mlflow.log_artifact(str(MODEL_PATH), artifact_path="model")
        mlflow.log_artifact(str(METRICS_PATH), artifact_path="metrics")

        print(f"Experiment: {experiment_name}")
        print(f"Git commit: {git_sha}")
        print(f"Dataset SHA-256: {dataset_hash}")
        print(f"Dataset rows: {len(df)}")
        print(f"Training samples: {len(y_train)}")
        print(f"Test samples: {len(y_test)}")
        print(f"Accuracy: {accuracy:.3f}")
        print(f"Weighted F1: {weighted_f1:.3f}")
        print("\nClassification report:")
        print(
            classification_report(
                y_test,
                predictions,
                zero_division=0,
            )
        )
        print(f"Model saved to: {MODEL_PATH}")
        print(f"Metrics saved to: {METRICS_PATH}")
        print(f"MLflow run ID: {mlflow.active_run().info.run_id}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--experiment-name",
        default="smart-waste-classifier",
    )
    parser.add_argument(
        "--c",
        type=float,
        default=1.0,
        help="Inverse regularization strength for LogisticRegression",
    )
    args = parser.parse_args()

    train_model(
        experiment_name=args.experiment_name,
        c_value=args.c,
    )
