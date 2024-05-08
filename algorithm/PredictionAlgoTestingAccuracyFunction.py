import json
import numpy as np

# Assuming the prediction functions and their dependencies have been defined/imported properly
from PredictionAlgo import predict_enrollment, filter_course_data
def load_data(file_path):
    """
    Load course data from a JSON file.
    
    Args:
        file_path (str): The path to the JSON file.
    
    Returns:
        dict: The loaded course data.
    """
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def calculate_metrics(actual, predicted):
    """
    Calculate MAE, RMSE, and R-squared manually.
    
    Args:
        actual (list): List of actual values.
        predicted (list): List of predicted values.
    
    Returns:
        tuple: A tuple containing MAE, RMSE, and R-squared values.
    """
    n = len(actual)
    mae = sum(abs(a - p) for a, p in zip(actual, predicted)) / n
    mse = sum((a - p) ** 2 for a, p in zip(actual, predicted)) / n
    rmse = np.sqrt(mse)
    mean_actual = sum(actual) / n
    ss_tot = sum((a - mean_actual) ** 2 for a in actual)
    ss_res = sum((a - p) ** 2 for a, p in zip(actual, predicted))
    r2 = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0  # Handling for constant actual values case
    return mae, rmse, r2

def backtest_predictions(data, course_ids):
    """
    Perform backtesting of the prediction algorithm by comparing predictions against actual enrollments.
    
    Args:
        data (list): List of dictionaries containing course data.
        course_ids (set): Set of course IDs.
    
    Returns:
        dict: A dictionary containing results of the backtesting.
    """
    results = {}
    for course_id in course_ids:
        course_data = filter_course_data(data, course_id)
        historical_terms = [d['session_term'] for d in course_data if 'total_enrollment' in d]
        historical_enrollments = [d['total_enrollment'] for d in course_data if 'total_enrollment' in d]

        predicted_enrollments = []
        for i in range(1, len(historical_terms)):
            temp_data = course_data[:i]
            _, predicted = predict_enrollment(temp_data, course_id)
            predicted_enrollments.append(predicted)

        mae, rmse, r2 = calculate_metrics(historical_enrollments[1:], predicted_enrollments)
        results[course_id] = {'MAE': mae, 'RMSE': rmse, 'R^2': r2}

    return results

def main():
    """
    Main function to perform backtesting of prediction algorithms.
    """
    file_path = '../data_alteration/summarized_course_data.json'
    course_data = load_data(file_path)
    course_ids = set([d['course_name'] for d in course_data])
    results = backtest_predictions(course_data, course_ids)

    for course_id, metrics in results.items():
        print(f"Results for {course_id}:")
        print(f"  MAE: {metrics['MAE']}")
        print(f"  RMSE: {metrics['RMSE']}")
        print(f"  R^2: {metrics['R^2']}")

if __name__ == "__main__":
    main()
