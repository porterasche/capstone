import pytest
import json
import numpy as np
from PredictionAlgo import read_json_data, filter_course_data, encode_terms, multiple_linear_regression, predict_enrollment

@pytest.fixture
def sample_course_data():
    return [
        {"course_name": "CSCI101", "session_term": "Spring 2022", "total_enrollment": 100},
        {"course_name": "CSCI101", "session_term": "Fall 2022", "total_enrollment": 120},
        {"course_name": "CSCI101", "session_term": "Spring 2023", "total_enrollment": 130},
        {"course_name": "MATH101", "session_term": "Spring 2022", "total_enrollment": 80},
        {"course_name": "MATH101", "session_term": "Fall 2022", "total_enrollment": 90},
    ]

def test_read_json_data(tmp_path):
    test_data = {"key": "value"}
    file_path = tmp_path / "test_data.json"
    with open(file_path, "w") as f:
        json.dump(test_data, f)
    assert read_json_data(file_path) == test_data

def test_filter_course_data(sample_course_data):
    filtered_data = filter_course_data(sample_course_data, "CSCI101")
    assert len(filtered_data) == 3
    assert all(record["course_name"] == "CSCI101" for record in filtered_data)

def test_encode_terms():
    terms = ["Spring 2022", "Fall 2022", "Spring 2023"]
    last_season = "Spring"
    encoded_terms, _, _ = encode_terms(terms, last_season)
    assert len(encoded_terms) == 3
    assert len(encoded_terms[0]) == 3  # Three elements for each term encoding

def test_multiple_linear_regression():
    X = np.array([[1, 0, 0], [0, 1, 1], [1, 1, 0]])
    y = np.array([10, 20, 30])
    weights = np.array([1, 1, 1])
    coefficients = multiple_linear_regression(X, y, weights)
    assert len(coefficients) == 4  # One intercept and three coefficients for features

def test_predict_enrollment(sample_course_data):
    future_term, predicted_enrollment = predict_enrollment(sample_course_data, "CSCI101")
    assert isinstance(future_term, str)
    assert isinstance(predicted_enrollment, int)


