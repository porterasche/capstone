import json
import numpy as np
from datetime import datetime

def read_json_data(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def aggregate_enrollment_by_term(course_data):
    enrollment_by_term = {}
    for section in course_data["sections"]:
        term = section["Date"].split(" - ")[0]
        year = datetime.strptime(term, "%b %d, %Y").year
        enrollment = int(section["Enrolled"])
        if year in enrollment_by_term:
            enrollment_by_term[year] += enrollment
        else:
            enrollment_by_term[year] = enrollment
    return enrollment_by_term

def simple_linear_regression(X, y):
    n = len(X)
    x_mean = np.mean(X)
    y_mean = np.mean(y)
    xy_mean = np.mean(X*y)
    x_square_mean = np.mean(X**2)
    
    b1 = (xy_mean - x_mean * y_mean) / (x_square_mean - x_mean**2)
    b0 = y_mean - b1 * x_mean
    
    return b0, b1

def predict_enrollment(b0, b1, year):
    return b0 + b1 * year

def backtest_model(enrollment_by_term):
    sorted_years = sorted(enrollment_by_term.keys())
    train_years = np.array(sorted_years[:-1])  # Exclude the most recent year
    test_year = np.array([sorted_years[-1]])  # Most recent year
    
    X_train = train_years
    y_train = np.array([enrollment_by_term[year] for year in train_years])
    
    b0, b1 = simple_linear_regression(X_train, y_train)
    
    predicted_enrollment = predict_enrollment(b0, b1, test_year[0])
    actual_enrollment = enrollment_by_term[test_year[0]]
    
    print(f"Predicted enrollment for {test_year[0]}: {int(predicted_enrollment)}")
    print(f"Actual enrollment for {test_year[0]}: {actual_enrollment}")
    
    accuracy = 100 - (abs(predicted_enrollment - actual_enrollment) / actual_enrollment) * 100
    print(f"Accuracy: {accuracy:.2f}%")

def main():
    file_path = "course_history.json"
    course_id = "CSCI 1200 CS PRINCIPLES"
    data = read_json_data(file_path)
    course_data = data[course_id]
    enrollment_by_term = aggregate_enrollment_by_term(course_data)
    
    backtest_model(enrollment_by_term)

if __name__ == "__main__":
    main()
