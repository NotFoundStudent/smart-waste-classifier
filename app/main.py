from pathlib import Path

import joblib
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = PROJECT_ROOT / "models" / "waste_model.joblib"

FEATURE_NAMES = ["weight_g", "moisture_pct", "magnetic"]
VALID_CATEGORIES = {"plastic", "metal", "paper", "organic"}


def load_model(model_path=MODEL_PATH):
    """Load the trained waste classification model."""
    model_path = Path(model_path)

    if not model_path.is_file():
        raise FileNotFoundError(f"Model not found: {model_path}")

    return joblib.load(model_path)


def predict_category(weight_g, moisture_pct, magnetic, model=None):
    """Predict a waste category from three numeric features."""
    values = {
        "weight_g": weight_g,
        "moisture_pct": moisture_pct,
        "magnetic": magnetic,
    }

    for name, value in values.items():
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError(f"{name} must be a number.")

    if weight_g <= 0:
        raise ValueError("weight_g must be greater than zero.")

    if not 0 <= moisture_pct <= 100:
        raise ValueError("moisture_pct must be between 0 and 100.")

    if magnetic not in (0, 1):
        raise ValueError("magnetic must be 0 or 1.")

    if model is None:
        model = load_model()

    features = pd.DataFrame(
        [[weight_g, moisture_pct, magnetic]],
        columns=FEATURE_NAMES,
    )

    prediction = model.predict(features)[0]

    if prediction not in VALID_CATEGORIES:
        raise ValueError(f"Model returned an unknown category: {prediction}")

    return str(prediction)


if __name__ == "__main__":
    result = predict_category(
        weight_g=30,
        moisture_pct=12,
        magnetic=0,
    )
    print(f"Predicted waste category: {result}")
