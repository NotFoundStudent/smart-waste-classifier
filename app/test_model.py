
import pytest

from app.main import MODEL_PATH, load_model, predict_category

VALID_CATEGORIES = {"plastic", "metal", "paper", "organic"}


def test_saved_model_exists_and_can_be_loaded():
    assert MODEL_PATH.is_file()

    model = load_model()

    assert hasattr(model, "predict")


def test_model_prediction_returns_valid_category():
    result = predict_category(
        weight_g=30,
        moisture_pct=12,
        magnetic=0,
    )

    assert result in VALID_CATEGORIES


def test_load_model_rejects_missing_file(tmp_path):
    missing_model = tmp_path / "missing_model.joblib"

    with pytest.raises(FileNotFoundError, match="Model not found"):
        load_model(missing_model)


def test_prediction_rejects_invalid_magnetic_value():
    with pytest.raises(ValueError, match="magnetic"):
        predict_category(
            weight_g=30,
            moisture_pct=12,
            magnetic=3,
        )
