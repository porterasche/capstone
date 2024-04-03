# Import necessary libraries
import json
import numpy as np
from datetime import datetime

# Function to read JSON data from a file
def read_json_data(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

# Function to filter data for a specific course based on its course ID
def filter_course_data(course_data, course_id):
    return [record for record in course_data if record['course_name'] == course_id]

# Function to encode terms into numerical values for regression
def encode_terms(terms):
    term_mapping = {}
    encoded_terms = []
    for term in terms:
        season, year = term.split()
        encoded = int(year) + (.0 if season == 'Spring' else .5)
        encoded_terms.append(encoded)
        term_mapping[encoded] = term
    return np.array(encoded_terms), term_mapping

# Function for performing simple linear regression
def simple_linear_regression(X, y):
    x_mean = np.mean(X)
    y_mean = np.mean(y)
    xy_mean = np.mean(X*y)
    x_square_mean = np.mean(X**2)
    
    b1 = (xy_mean - x_mean * y_mean) / (x_square_mean - x_mean**2)
    b0 = y_mean - b1 * x_mean
    
    return b0, b1

# Modified predict_enrollment function to exclude the most recent term for prediction
def predict_enrollment(course_data, course_id):
    specific_course_data = filter_course_data(course_data, course_id)
    
    # Use only terms with non-zero enrollment for prediction
    valid_data_for_prediction = [record for record in specific_course_data if record.get('total_enrollment', -1) > 0]
    
    if not valid_data_for_prediction:
        return "No valid data for prediction", 0
    
    # Sort and exclude the most recent term data
    valid_data_for_prediction.sort(key=lambda x: x["session_term"])
    excluded_term_data = valid_data_for_prediction.pop()
    
    terms = [record["session_term"] for record in valid_data_for_prediction]
    enrollments = [record["total_enrollment"] for record in valid_data_for_prediction]
    
    X, _ = encode_terms(terms)
    y = np.array(enrollments)
    
    b0, b1 = simple_linear_regression(X, y)
    
    # Predict for the next term, considering the latest term in the dataset is now excluded
    if X[-1] % 1 == 0:
        future_encoded = X[-1] + 0.5
    else:
        future_encoded = np.ceil(X[-1])
    
    predicted_enrollment = b0 + b1 * future_encoded
    
    future_term = 'Fall' if future_encoded % 1 > 0 else 'Spring'
    future_year = int(future_encoded) if future_term == 'Fall' else int(future_encoded + 1)
    future_term_str = f"{future_term} {future_year}"
    
    # Actual enrollment from the excluded term for comparison
    actual_enrollment = excluded_term_data["total_enrollment"]
    
    return future_term_str, int(predicted_enrollment), actual_enrollment

# Main function to run the program
def main():
    file_path = "../data_alteration/summarized_course_data.json"  # Example file path; adjust as needed
    course_id = "CSCI 1200 CS PRINCIPLES"  # Example course ID
    data = read_json_data(file_path)
    future_term, predicted_enrollment, actual_enrollment = predict_enrollment(data, course_id)
    print(f"Predicted enrollment for {future_term}: {predicted_enrollment}")
    print(f"Actual enrollment for comparison: {actual_enrollment}")

# The call to main() is commented out to prevent automatic execution in this interface.
# If you're implementing this in a standalone script, uncomment the following line.
main()
