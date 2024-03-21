import json

def read_json_data(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def extract_course_names(data):
    return list(data.keys())

def save_course_names(course_names, output_file_path):
    with open(output_file_path, 'w') as file:
        json.dump(course_names, file, indent=4)

def main():
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
