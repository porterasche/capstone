import json
import re

def extract_prereqs(json_data):
    """
    Extract prerequisite course IDs from a JSON data dictionary.

    This function searches for instances of 4 letters followed by 4 numbers in the 'prereqs' field of each entry in the JSON data.
    It then replaces the original 'prereqs' field with a list of extracted prerequisite course IDs.

    Args:
        json_data (list of dict): The JSON data containing course information.

    Returns:
        list of dict: The JSON data with the 'prereqs' field updated to contain a list of prerequisite course IDs.
    """
    # Compile the regex pattern to match 4 letters followed by 4 numbers
    pattern = re.compile(r'\b[A-Za-z]{4}\d{4}\b')

    # Iterate over each entry in the JSON data
    for entry in json_data:
        if 'prereqs' in entry:
            # Extract instances of 4 letters followed by 4 numbers from the prereqs field
            prereqs_list = pattern.findall(entry['prereqs'])
            # Reassign the prereqs field to be a list of instances found
            entry['prereqs'] = prereqs_list

    return json_data

def main():
    """
    Main function to extract and print updated prerequisite course IDs from a JSON file.
    """
    # Read the JSON file
    with open('courses.json', 'r') as file:
        json_data = json.load(file)

    # Extract and reassign prereqs
    updated_json_data = extract_prereqs(json_data)

    # Print the updated JSON data
    print(json.dumps(updated_json_data, indent=4))

if __name__ == "__main__":
    main()
