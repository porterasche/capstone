import json
import numpy as np

def read_json_data(file_path):
    """
    Reads JSON data from a file.
    
    Args:
        file_path (str): The path to the JSON file.
    
    Returns:
        dict: The loaded JSON data.
    """
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def filter_course_data(course_data, course_id):
    """
    Filters data for a specific course based on its course_name.
    
    Args:
        course_data (list): List of dictionaries containing course data.
        course_id (str): The course ID to filter data for.
    
    Returns:
        list: Filtered list of dictionaries containing course data for the specified course.
    """
    return [record for record in course_data if record['course_name'] == course_id]

def encode_terms(terms):
    """
    Encode term strings into numerical and seasonal values for regression.
    Using sine and cosine to capture cyclical nature of terms and adding seasonal weights.
    
    Args:
        terms (list): List of term strings in the format 'Season Year'.
    
    Returns:
        tuple: A tuple containing encoded terms, term mapping, and weights.
    """
    term_mapping = {}
    encoded_terms = []
    weights = []
    for term in terms:
        season, year = term.split()
        year = int(year)
        # Seasonal encoding using sine and cosine
        if season == 'Spring':
            encoded = [np.sin(2 * np.pi * year / 6), np.cos(2 * np.pi * year / 6), 0]  # Spring
        else:
            encoded = [np.sin(2 * np.pi * year / 6), np.cos(2 * np.pi * year / 6), 1]  # Fall
        # Assign weights higher for the same season to emphasize seasonal cycles
        weight = 1.5 if season == 'Spring' else 1.0
        encoded_terms.append(encoded)
        term_mapping[year + (0.5 if season == 'Fall' else 0)] = term
        weights.append(weight)
    return np.array(encoded_terms), term_mapping, np.array(weights)

def multiple_linear_regression(X, y, weights):
    """
    Performs weighted linear regression to handle seasonal variations more effectively.
    
    Args:
        X (numpy.ndarray): Input features.
        y (numpy.ndarray): Target values.
        weights (numpy.ndarray): Weights for each data point.
    
    Returns:
        numpy.ndarray: Coefficients of the linear regression model.
    """
    # Apply weights to both X and y
    weighted_X = X * weights[:, None]  # Apply weights to each feature
    weighted_y = y * weights
    # Adding a constant term for intercept
    X_with_intercept = np.hstack([np.ones((X.shape[0], 1)), weighted_X])
    # Compute weighted least squares regression
    coefficients = np.linalg.lstsq(X_with_intercept, weighted_y, rcond=None)[0]
    return coefficients

def predict_enrollment(course_data, course_id):
    """
    Predicts the next term's enrollment based on linear regression, using weighted seasonal adjustments.
    
    Args:
        course_data (list): List of dictionaries containing course data.
        course_id (str): The course ID to predict enrollment for.
    
    Returns:
        tuple: A tuple containing course ID, future term, and predicted enrollment.
    """
    specific_course_data = filter_course_data(course_data, course_id)
    valid_data_for_prediction = [record for record in specific_course_data if record.get('total_enrollment', -1) > 0]
    
    if not valid_data_for_prediction:
        return None
    
    terms = [record["session_term"] for record in valid_data_for_prediction]
    enrollments = [record["total_enrollment"] for record in valid_data_for_prediction]
    
    X, term_mapping, weights = encode_terms(terms)
    y = np.array(enrollments)
    
    coefficients = multiple_linear_regression(X, y, weights)
    
    last_term = terms[-1]
    last_season = 'Spring' if 'Spring' in last_term else 'Fall'
    next_season = 'Fall' if last_season == 'Spring' else 'Spring'
    next_year = int(last_term.split()[1]) + (1 if next_season == 'Spring' else 0)
    next_term_encoded = [np.sin(2 * np.pi * next_year / 6), np.cos(2 * np.pi * next_year / 6), 1 if next_season == 'Fall' else 0]
    
    predicted_enrollment = np.dot(coefficients[1:], next_term_encoded) + coefficients[0]
    future_term_str = f"{next_season} {next_year}"
    return (course_id, future_term_str, int(predicted_enrollment))

def main():
    """
    Main function to predict enrollments for courses.
    """
    course_names_file = "course_names.json"
    course_names = read_json_data(course_names_file)
    data_file_path = "../data_alteration/summarized_course_data.json"
    course_data = read_json_data(data_file_path)

    predictions = []
    for course_id in course_names:
        result = predict_enrollment(course_data, course_id)
        if result:
            predictions.append(result)

    # Sort predictions by predicted enrollment in descending order
    predictions.sort(key=lambda x: x[2], reverse=True)

    # Save all predictions to a file
    with open("predicted_enrollments.txt", "w") as file:
        for prediction in predictions:
            file.write(f"{prediction[0]}, {prediction[1]}, {prediction[2]}\n")

    # Display the top 10 classes with the highest predicted enrollments
    print("Top 10 Classes by Predicted Enrollment:")
    for prediction in predictions[:10]:
        print(f"{prediction[0]} in {prediction[1]}: {prediction[2]}")

if __name__ == "__main__":
    main()
