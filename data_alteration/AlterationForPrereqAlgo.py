import json
from datetime import datetime

def parse_term(term):
    """
    Convert a session term string to a datetime object for easy comparison.

    Args:
        term (str): The session term string, e.g., 'Spring 2019'.

    Returns:
        datetime: A datetime object representing the session term.
    """
    term_parts = term.split()
    season, year = term_parts[0], int(term_parts[1])
    month = {'Spring': 1, 'Fall': 9}.get(season, 1)
    return datetime(year, month, 1)

def normalize_course_id(course_name):
    """
    Normalize course names to match the format of the course IDs in the prerequisites file.

    Args:
        course_name (str): The course name to be normalized.

    Returns:
        str: The normalized course ID.
    """
    return course_name.replace(" ", "").upper()[:8]  # Only take first 8 characters

def load_cleaned_courses(course_file):
    """
    Load the cleaned course data which contains the course IDs and their prerequisites.

    Args:
        course_file (str): The path to the cleaned course data file.

    Returns:
        dict: A dictionary mapping course IDs to their prerequisites.
    """
    with open(course_file, 'r') as file:
        courses = json.load(file)
    # Map by first 8 characters of course ID to handle cases where IDs are truncated or normalized
    return {course['id'][:8]: course['prereqs'] for course in courses}

def load_and_transform_data(enrollment_file, course_prereqs):
    """
    Load JSON enrollment data, aggregate it by course to find the most recent enrollment,
    and add prerequisites from the provided data, focusing on courses.

    Args:
        enrollment_file (str): The path to the enrollment data file.
        course_prereqs (dict): A dictionary mapping course IDs to their prerequisites.

    Returns:
        dict: Transformed data with aggregated enrollment and prerequisites for each course.
    """
    with open(enrollment_file, 'r') as file:
        enrollment_data = json.load(file)

    today = datetime.today()
    course_aggregate = {}

    for entry in enrollment_data:
        course_name = entry["course_name"]
        normalized_id = normalize_course_id(course_name)

        if parse_term(entry["session_term"]) > today or entry["total_enrollment"] == 0:
            continue

        if (normalized_id not in course_aggregate or
            course_aggregate[normalized_id]['term_date'] < parse_term(entry["session_term"])):
            course_aggregate[normalized_id] = {
                'term_date': parse_term(entry["session_term"]),
                'enrollment': entry["total_enrollment"],
                'prerequisites': course_prereqs.get(normalized_id, [])
            }

    # Prepare data in the required format
    transformed_data = {}
    for course_id, info in course_aggregate.items():
        transformed_data[course_id] = {
            'enrollment': info['enrollment'],
            'prerequisites': info['prerequisites']
        }

    return transformed_data

def save_transformed_data(transformed_data, output_file):
    """
    Save the transformed data to a new JSON file.

    Args:
        transformed_data (dict): The transformed data to be saved.
        output_file (str): The path to the output JSON file.
    """
    with open(output_file, 'w') as file:
        json.dump(transformed_data, file, indent=4)

def main():
    """
    Main function to load, transform, and save enrollment data.
    """
    enrollment_file_path = "summarized_course_data.json"
    cleaned_course_file_path = "cleaned_courses.json"
    output_file_path = "../algorithm/transformed_course_data.json"

    # Load cleaned course data
    cleaned_course_prereqs = load_cleaned_courses(cleaned_course_file_path)
    # Transform data
    transformed_data = load_and_transform_data(enrollment_file_path, cleaned_course_prereqs)
    save_transformed_data(transformed_data, output_file_path)
    print("Data has been transformed and saved to", output_file_path)

if __name__ == "__main__":
    main()
