import json
from datetime import datetime

def process_course_data(course_history):
    """
    Process course data to summarize enrollment information based on session terms.

    Args:
        course_history (dict): Dictionary containing course history data.

    Returns:
        list: List of dictionaries containing summarized enrollment information.
    """
    summarized_data = {}

    def determine_session(date_str):
        """
        Determine the session term based on a given date string.

        Args:
            date_str (str): Date string in the format "MMM DD, YYYY".

        Returns:
            str or None: Session term string (e.g., "Spring 2023") if valid, otherwise None.
        """
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

# Load the JSON data
with open('../webscraper/course_history.json', 'r') as file:
    course_history = json.load(file)

# Process and save the corrected data
corrected_data = process_course_data(course_history)
with open('summarized_course_data.json', 'w') as outfile:
    json.dump(corrected_data, outfile, indent=4)

print("Data processing corrected. Check summarized_course_data.json for the output.")
