import json
from datetime import datetime

# Load the JSON data
with open('../webscraper/course_history.json', 'r') as file:
    course_history = json.load(file)

# Initialize a dictionary to hold the summarized data
summarized_data = {}

# Function to determine the session term based on date
def process_course_data(course_history):
    summarized_data = {}

    def determine_session(date_str):
        date = datetime.strptime(date_str, "%b %d, %Y")
        if 1 <= date.month <= 5:
            return f'Spring {date.year}'
        elif 8 <= date.month <= 12:
            return f'Fall {date.year}'
        return None

    for course_name, course_info in course_history.items():
        for section in course_info['sections']:
            session_term = determine_session(section['Date'].split(' - ')[0])
            if session_term:
                enrolled = int(section['Enrolled'])
                # Create a unique key for each course and term
                course_term_key = f"{course_name}-{session_term}"
                if course_term_key in summarized_data:
                    # Add to the existing enrollment
                    summarized_data[course_term_key]['total_enrollment'] += enrolled
                else:
                    # Initialize data for new course-term combination
                    summarized_data[course_term_key] = {
                        'course_name': course_name,
                        'total_enrollment': enrolled,
                        'session_term': session_term
                    }

    # Convert to a list for output
    output_data = list(summarized_data.values())
    return output_data

# Assume the data is loaded into `course_history`

# Process and save the corrected data
corrected_data = process_course_data(course_history)
with open('summarized_course_data.json', 'w') as outfile:
    json.dump(corrected_data, outfile, indent=4)

print("Data processing corrected. Check summarized_course_data.json for the output.")
