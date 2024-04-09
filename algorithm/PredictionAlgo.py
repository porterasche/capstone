import json
import numpy as np
from datetime import datetime

def read_json_data(file_path):
    """
    Reads JSON data from a file.

    @param file_path The path of the file to read.
    @return The JSON data read from the file.
    """
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def filter_course_data(course_data, course_id):
    """
    Filters data for a specific course based on its course_name.

    @param course_data The dataset containing course records.
    @param course_id The ID of the course to filter for.
    @return A list of records for the specified course.
    """
    return [record for record in course_data if record['course_name'] == course_id]

def encode_terms(terms):
    """
    Encode term strings into numerical values for regression.

    Terms are split into components (e.g., 'Spring 2019') and encoded numerically,
    with Spring as .0 and Fall as .5 to represent parts of the year.

    @param terms A list of term strings to encode.
    @return A tuple containing an array of encoded terms and a mapping of encoded terms to their original strings.
    """
    term_mapping = {}
    encoded_terms = []
    for term in terms:
        season, year = term.split()
        encoded = int(year) + (.0 if season == 'Spring' else .5)
        encoded_terms.append(encoded)
        term_mapping[encoded] = term
    return np.array(encoded_terms), term_mapping

def simple_linear_regression(X, y):
    """
    Performs simple linear regression on the data.

    @param X The independent variable data.
    @param y The dependent variable data.
    @return The intercept and slope of the regression line.
    """
    x_mean = np.mean(X)
    y_mean = np.mean(y)
    xy_mean = np.mean(X*y)
    x_square_mean = np.mean(X**2)
    
    b1 = (xy_mean - x_mean * y_mean) / (x_square_mean - x_mean**2)
    b0 = y_mean - b1 * x_mean
    
    return b0, b1

def predict_enrollment(course_data, course_id):
    """
    Predicts the next term's enrollment based on linear regression, accurately handling term transitions.

    @param course_data The dataset of course records.
    @param course_id The ID of the course for which to predict enrollment.
    @return A tuple containing the string representation of the future term and the predicted enrollment as an integer.
    """
    specific_course_data = filter_course_data(course_data, course_id)
    valid_data_for_prediction = [record for record in specific_course_data if record.get('total_enrollment', -1) > 0]
    
    if not valid_data_for_prediction:
        return "No valid data for prediction", 0
    
    terms = [record["session_term"] for record in valid_data_for_prediction]
    enrollments = [record["total_enrollment"] for record in valid_data_for_prediction]
    
    X, _ = encode_terms(terms)
    y = np.array(enrollments)
    
    b0, b1 = simple_linear_regression(X, y)
    
    future_encoded = X[-1] + 0.5 if X[-1] % 1 == 0 else np.ceil(X[-1])
    predicted_enrollment = b0 + b1 * future_encoded
    
    future_term = 'Fall' if future_encoded % 1 > 0 else 'Spring'
    future_year = int(future_encoded) if future_term == 'Fall' else int(future_encoded + 1)
    future_term_str = f"{future_term} {future_year}"
    
    return future_term_str, int(predicted_enrollment)

def choose_course(course_names_file):
    """
    Prompts the user to choose a course from a list.

    @param course_names_file The path of the file containing course names.
    @return The selected course name.
    """
    course_names = read_json_data(course_names_file)
    for i, course in enumerate(course_names, start=1):
        print(f"{i}. {course}")
    choice = int(input("Select a course by number: ")) - 1
    return course_names[choice]

def main():
    """
    Main function to predict course enrollment.
    """
    course_names_file = "course_names.json"
    course_id = choose_course(course_names_file)
    file_path = "../data_alteration/summarized_course_data.json"
    data = read_json_data(file_path)
    future_term, predicted_enrollment = predict_enrollment(data, course_id)
    print(f"Predicted enrollment for {future_term}: {predicted_enrollment}")

if __name__ == "__main__":
    main()