import pytest
import json
import numpy as np
from PredictionAlgoTestingAccuracyFunction import load_data, calculate_metrics, backtest_predictions

@pytest.fixture
def sample_course_data():
    return [
        {"course_name": "CSCI101", "session_term": "Spring 2022", "total_enrollment": 100},
        {"course_name": "CSCI101", "session_term": "Fall 2022", "total_enrollment": 120},
        {"course_name": "CSCI101", "session_term": "Spring 2023", "total_enrollment": 130},
        {"course_name": "MATH101", "session_term": "Spring 2022", "total_enrollment": 80},
        {"course_name": "MATH101", "session_term": "Fall 2022", "total_enrollment": 90},
    ]

def test_load_data(tmp_path):
    test_data = {"key": "value"}
    file_path = tmp_path / "test_data.json"
    with open(file_path, "w") as f:
        json.dump(test_data, f)
    assert load_data(file_path) == test_data

def test_calculate_metrics():
    actual = [10, 20, 30]
    predicted = [12, 18, 32]
    mae, rmse, r2 = calculate_metrics(actual, predicted)
    assert mae == 2
    assert rmse == pytest.approx(2.0)  # Approximate value due to floating-point precision
    assert r2 == pytest.approx(0.94)  # Approximate value due to floating-point precision

def test_backtest_predictions(sample_course_data):
    course_ids = {"CSCI101", "MATH101"}
    results = backtest_predictions(sample_course_data, course_ids)
    assert isinstance(results, dict)
    assert "CSCI101" in results
    assert "MAE" in results["CSCI101"]
    assert "RMSE" in results["CSCI101"]
    assert "R^2" in results["CSCI101"]
    assert "MATH101" in results
    assert "MAE" in results["MATH101"]
    assert "RMSE" in results["MATH101"]
    assert "R^2" in results["MATH101"]


