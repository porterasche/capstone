import json
import numpy as np

def read_json_data(file_path):
    """
    Reads JSON data from a file.
    
    Args:
        file_path (str): The path to the JSON file.
    
    Returns:
        dict: The JSON data loaded from the file.
    """
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def filter_course_data(course_data, course_id):
    """
    Filters data for a specific course based on its course_name.
    
    Args:
        course_data (list): List of dictionaries containing course data.
        course_id (str): ID of the course.
    
    Returns:
        list: Filtered list of dictionaries containing course data for the specified course ID.
    """
    return [record for record in course_data if record['course_name'] == course_id]

def encode_terms(terms, last_season):
    """
    Encode term strings into numerical and seasonal values for regression,
    and generate weights based on seasonal alignment.
    
    Args:
        terms (list): List of term strings.
        last_season (str): Season of the last recorded term.
    
    Returns:
        tuple: Encoded terms, term mapping, and weights.
    """
    term_mapping = {}
    encoded_terms = []
    weights = []
    for term in terms:
        season, year = term.split()
        year = int(year)
        weight = 1.5 if season == last_season else 1.0  # Increase weight for terms in the same season
        if season == 'Spring':
            encoded = [np.sin(2 * np.pi * year / 6), np.cos(2 * np.pi * year / 6), 0]  # Spring
        else:
            encoded = [np.sin(2 * np.pi * year / 6), np.cos(2 * np.pi * year / 6), 1]  # Fall
        encoded_terms.append(encoded)
        term_mapping[year + (0.5 if season == 'Fall' else 0)] = term
        weights.append(weight)
    return np.array(encoded_terms), term_mapping, np.array(weights)

def multiple_linear_regression(X, y, weights):
    """
    Handles multiple factors including seasonal variations for regression,
    applying weights to emphasize data from matching seasons.
    
    Args:
        X (numpy.ndarray): Input features.
        y (numpy.ndarray): Target values.
        weights (numpy.ndarray): Weights for the data.
    
    Returns:
        numpy.ndarray: Coefficients of the linear regression model.
    """
    # Normalize weights and apply them
    weights = np.sqrt(weights)
    X_weighted = X * weights[:, np.newaxis]
    y_weighted = y * weights

    X_design = np.hstack([np.ones((X_weighted.shape[0], 1)), X_weighted])
    coefficients = np.linalg.lstsq(X_design, y_weighted, rcond=None)[0]
    return coefficients

def predict_enrollment(course_data, course_id):
    """
    Predicts enrollment based on historical data and seasonal trends,
    emphasizing data from the same seasonal cycle.
    
    Args:
        course_data (list): List of dictionaries containing course data.
        course_id (str): ID of the course.
    
    Returns:
        tuple: A tuple containing the future term and the predicted enrollment.
    """
    specific_course_data = filter_course_data(course_data, course_id)
    valid_data_for_prediction = [record for record in specific_course_data if record.get('total_enrollment', -1) > 0]
    if not valid_data_for_prediction:
        return "No valid data for prediction", 0

    terms = [record["session_term"] for record in valid_data_for_prediction]
    enrollments = [record["total_enrollment"] for record in valid_data_for_prediction]
    last_season = terms[-1].split()[0]  # Extract season from the last recorded term

    X, _, weights = encode_terms(terms, last_season)
    y = np.array(enrollments)

    coefficients = multiple_linear_regression(X, y, weights)

    last_year = int(terms[-1].split()[1])
    next_season = 'Fall' if last_season == 'Spring' else 'Spring'
    next_year = last_year if next_season == 'Fall' else last_year + 1
    next_term_encoded = [np.sin(2 * np.pi * next_year / 6), np.cos(2 * np.pi * next_year / 6), 1 if next_season == 'Fall' else 0]

    predicted_enrollment = np.dot(coefficients, [1] + next_term_encoded)
    future_term_str = f"{next_season} {next_year}"
    return (future_term_str, int(predicted_enrollment))

def main():
    """
    Main function to predict enrollments for courses based on historical data.
    """
    course_names_file = "course_names.json"
    course_names = read_json_data(course_names_file)
    
    print("Available Courses:")
    for i, course in enumerate(course_names, start=1):
        print(f"{i}. {course}")
    choice = int(input("Select a course by number: ")) - 1
    course_id = course_names[choice]
    
    data_file_path = "../data_alteration/summarized_course_data.json"
    course_data = read_json_data(data_file_path)
    
    future_term, predicted_enrollment = predict_enrollment(course_data, course_id)
    print(f"Predicted enrollment for {course_id} in {future_term}: {predicted_enrollment}")

if __name__ == "__main__":
    main()
