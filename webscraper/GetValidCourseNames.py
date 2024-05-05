import json

def read_json_data(file_path):
    """
    Read JSON data from a file.

    Args:
        file_path (str): The path to the JSON file.

    Returns:
        dict: The JSON data read from the file.
    """
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def extract_course_names(data):
    """
    Extract course names from JSON data.

    Args:
        data (dict): JSON data containing course information.

    Returns:
        list: A list of course names extracted from the JSON data.
    """
    return list(data.keys())

def save_course_names(course_names, output_file_path):
    """
    Save course names to a JSON file.

    Args:
        course_names (list): A list of course names to be saved.
        output_file_path (str): The path to the output JSON file.
    """
    with open(output_file_path, 'w') as file:
        json.dump(course_names, file, indent=4)

def main():
    """
    Main function to extract and save course names from course history data.
    """
    input_file_path = 'course_history.json'
    output_file_path = 'course_names.json'
    
    # Read the course history data
    data = read_json_data(input_file_path)
    
    # Extract course names
    course_names = extract_course_names(data)
    
    # Save course names to a new JSON file
    save_course_names(course_names, output_file_path)
    print(f"Course names have been saved to {output_file_path}.")

if __name__ == "__main__":
    main()
