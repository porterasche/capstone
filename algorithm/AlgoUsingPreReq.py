import json
import numpy as np

def read_json_data(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def get_prereq_data(course_data, course_id, decay_factor=0.85):
    """
    Calculates the weighted sum of enrollments from prerequisite courses.
    """
    course_info = course_data.get(course_id, {})
    prereqs = course_info.get('prerequisites', [])
    weighted_enrollments = 0
    for prereq in prereqs:
        prereq_enrollment = course_data.get(prereq, {}).get('enrollment', 0)
        # Apply decay factor to account for dropouts and failures
        weighted_enrollments += prereq_enrollment * decay_factor
    return weighted_enrollments

def predict_enrollment_with_prereqs(course_data, course_id):
    """
    Predicts enrollment for a course based on the enrollments of its prerequisites.
    """
    if course_id not in course_data:
        return "No data available for this course", 0

    # Get weighted enrollments from prerequisites
    prereq_weighted_enrollments = get_prereq_data(course_data, course_id)

    # Simple model: Assume the enrollment will be proportional to the prereq enrollments
    # This is a placeholder for a more complex regression model you might use
    predicted_enrollment = prereq_weighted_enrollments  # Here you could apply a regression model

    return course_id, int(predicted_enrollment)

def main():
    data_file_path = "course_data.json"
    course_data = read_json_data(data_file_path)

    predictions = []
    for course_id in course_data.keys():
        _, predicted_enrollment = predict_enrollment_with_prereqs(course_data, course_id)
        predictions.append((course_id, predicted_enrollment))

    # Sort predictions by predicted enrollment in descending order
    predictions.sort(key=lambda x: x[1], reverse=True)

    # Save all predictions to a file
    with open("predicted_enrollments_with_prereqs.txt", "w") as file:
        for prediction in predictions:
            file.write(f"{prediction[0]}, {prediction[1]}\n")

    # Optionally, print predictions
    print("Predictions with Prerequisites considered:")
    for prediction in predictions:
        print(f"Course ID: {prediction[0]}, Predicted Enrollment: {prediction[1]}")

if __name__ == "__main__":
    main()
