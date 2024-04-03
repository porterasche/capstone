import json
import numpy as np
from datetime import datetime

def read_json_data(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def filter_course_data(course_data, course_id):
    """Filters data for a specific course based on its course_name."""
    return [record for record in course_data if record['course_name'] == course_id]

def encode_terms(terms):
    """Encode term strings into numerical values for regression."""
    term_mapping = {}
    encoded_terms = []
    for term in terms:
        # Split the term into its components (e.g., 'Spring 2019' -> ['Spring', '2019'])
        season, year = term.split()
        # Encode 'Spring' as .0 and 'Fall' as .5 to represent parts of the year
        encoded = int(year) + (.0 if season == 'Spring' else .5)
        encoded_terms.append(encoded)
        term_mapping[encoded] = term
    return np.array(encoded_terms), term_mapping

def simple_linear_regression(X, y):
    """Performs simple linear regression on the data."""
    x_mean = np.mean(X)
    y_mean = np.mean(y)
    xy_mean = np.mean(X*y)
    x_square_mean = np.mean(X**2)
    
    b1 = (xy_mean - x_mean * y_mean) / (x_square_mean - x_mean**2)
    b0 = y_mean - b1 * x_mean
    
    return b0, b1

def predict_enrollment(course_data, course_id):
    """Predicts the next term's enrollment based on linear regression, accurately handling term transitions."""
    # Filter course data for the specified course_id
    specific_course_data = filter_course_data(course_data, course_id)
    
    # Use only terms with non-zero enrollment for prediction basis
    valid_data_for_prediction = [record for record in specific_course_data if record.get('total_enrollment', -1) > 0]
    
    if not valid_data_for_prediction:
        return "No valid data for prediction", 0
    
    # Extract terms and enrollment data
    terms = [record["session_term"] for record in valid_data_for_prediction]
    enrollments = [record["total_enrollment"] for record in valid_data_for_prediction]
    
    X, _ = encode_terms(terms)
    y = np.array(enrollments)
    
    b0, b1 = simple_linear_regression(X, y)
    
    # Correctly identify the next term, considering the transition from Spring to Fall or Fall to next Spring
    if X[-1] % 1 == 0:  # If the most recent term is Spring (.0), the next is Fall of the same year (.5)
        future_encoded = X[-1] + 0.5
    else:  # If the most recent term is Fall (.5), the next is Spring of the next year, so round up and add .0
        future_encoded = np.ceil(X[-1])

    predicted_enrollment = b0 + b1 * future_encoded
    
    # Decode the future term
    future_term = 'Fall' if future_encoded % 1 > 0 else 'Spring'
    future_year = int(future_encoded) if future_term == 'Fall' else int(future_encoded + 1)
    future_term_str = f"{future_term} {future_year}"
    
    return future_term_str, int(predicted_enrollment)





def main():
    file_path = "../data_alteration/summarized_course_data.json"
    course_id = "CSCI 1200 CS PRINCIPLES"  # Example course ID
    data = read_json_data(file_path)
    future_term, predicted_enrollment = predict_enrollment(data, course_id)
    print(f"Predicted enrollment for {future_term}: {predicted_enrollment}")

if __name__ == "__main__":
    main()
