import json
import numpy as np

def read_json_data(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def get_prereq_data(course_data, course_id):
    """
    Calculates the average enrollments from prerequisite courses, with a variable decay factor
    depending on the course level.
    """
    course_info = course_data.get(course_id, {})
    prereqs = course_info.get('prerequisites', [])
    total_enrollment = 0
    prereq_count = len(prereqs)

    # Define the decay factors
    standard_decay_factor = 0.45
    high_decay_factor = 0.35  # Higher decay for beginner courses

    # Determine the decay factor for the current course
    decay_factor = high_decay_factor if course_id.startswith('CSCI1') or course_id.startswith('CSCI2') else standard_decay_factor

    # Only proceed if there are prerequisites
    if prereq_count > 0:
        for prereq in prereqs:
            prereq_enrollment = course_data.get(prereq, {}).get('enrollment', 0)
            total_enrollment += prereq_enrollment
        # Calculate the average and apply decay factor
        average_enrollment = (total_enrollment / prereq_count) * decay_factor
    else:
        # If there are no prerequisites, return a default average enrollment value
        average_enrollment = 50  # Default value might need adjustment

    return average_enrollment



def predict_enrollment_with_prereqs(course_data, course_id):
    """
    Predicts enrollment for a course based on the average enrollments of its prerequisites.
    """
    if course_id not in course_data:
        return "No data available for this course", 0

    # Get average enrollments from prerequisites
    prereq_average_enrollments = get_prereq_data(course_data, course_id)

    # Simple model: Assume the enrollment will be similar to the average prereq enrollments
    predicted_enrollment = prereq_average_enrollments

    return course_id, int(predicted_enrollment)


def main():
    data_file_path = "transformed_course_data.json"
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
