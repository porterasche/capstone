import json
import re

def extract_prereqs(json_data):
    """
    Extract prerequisite codes from the 'prereqs' field of each entry in the JSON data.

    This function iterates over each entry in the JSON data, extracts prerequisite codes
    from the 'prereqs' field using a regular expression pattern, and reassigns the 'prereqs'
    field to be a list of extracted prerequisite codes.

    Args:
        json_data (list): List of dictionaries representing JSON data.

    Returns:
        list: Updated JSON data with 'prereqs' field replaced by a list of prerequisite codes.
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
    Main function to read JSON data from a file, clean it, and write it back to another file.
    """
    # Read the JSON file
    with open('courses.json', 'r') as file:
        json_data = json.load(file)

    # Extract and reassign prereqs
    updated_json_data = extract_prereqs(json_data)

    # Print the updated JSON data

    # Write the updated JSON data to a new file
    with open('cleaned_courses.json', 'w') as file:
        file.write(json.dumps(updated_json_data, indent=4))


if __name__ == "__main__":
    main()
