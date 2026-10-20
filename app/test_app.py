import pytest

from app.main import predict_category


class FakeModel:
    """A tiny model substitute for testing input validation."""

    def predict(self, features):
        return ["plastic"]


def test_valid_input_returns_category():
    result = predict_category(30, 12, 0, model=FakeModel())
    assert result == "plastic"


@pytest.mark.parametrize(
    "weight, moisture, magnetic",
    [
        (0, 12, 0),
        (-1, 12, 0),
        (30, -1, 0),
        (30, 101, 0),
        (30, 12, 2),
    ],
)
def test_invalid_numeric_ranges_are_rejected(weight, moisture, magnetic):
    with pytest.raises(ValueError):
        predict_category(weight, moisture, magnetic, model=FakeModel())


@pytest.mark.parametrize(
    "weight, moisture, magnetic",
    [
        ("30", 12, 0),
        (30, None, 0),
        (30, 12, True),
    ],
)
def test_invalid_types_are_rejected(weight, moisture, magnetic):
    with pytest.raises(ValueError):
        predict_category(weight, moisture, magnetic, model=FakeModel())


def test_unknown_model_category_is_rejected():
    class UnknownCategoryModel:
        def predict(self, features):
            return ["unknown"]

    with pytest.raises(ValueError, match="unknown category"):
        predict_category(30, 12, 0, model=UnknownCategoryModel())
