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
        term = section["Date"].split(" - ")[0]  # Assumes term starts with the date
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
    
    # Calculating slope (b1) and intercept (b0)
    b1 = (xy_mean - x_mean * y_mean) / (x_square_mean - x_mean**2)
    b0 = y_mean - b1 * x_mean
    
    return b0, b1

def predict_enrollment(enrollment_by_term):
    X = np.array(list(enrollment_by_term.keys())).reshape(-1, 1).flatten()  # Years
    y = np.array(list(enrollment_by_term.values()))  # Enrollment numbers
    
    b0, b1 = simple_linear_regression(X, y)
    future_year = X[-1] + 1  # Predicting the next year
    predicted_enrollment = b0 + b1 * future_year
    return future_year, predicted_enrollment


def main():
    file_path = "course_history.json"
    course_id = "CSCI 1200 CS PRINCIPLES"  # Example course ID
    data = read_json_data(file_path)
    course_data = data[course_id]
    enrollment_by_term = aggregate_enrollment_by_term(course_data)
    future_year, predicted_enrollment = predict_enrollment(enrollment_by_term)
    print(f"Predicted enrollment for {future_year}: {int(predicted_enrollment)}")

if __name__ == "__main__":
    main()
