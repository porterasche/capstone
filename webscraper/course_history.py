import requests
from bs4 import BeautifulSoup
import json
import csv
import re

# USING PYTHON 3.12.2 (https://www.python.org/downloads/)
# INSTALL REQUIRED EXTENSIONS WITH THESE COMMANDS
# python -m pip install requests
# python -m pip install beautifulsoup4

# beautifulsoup4 documentation: https://beautiful-soup-4.readthedocs.io/en/latest/

## Setup list of majors
majors = []
with open('majors.txt', 'r') as majors_file:
    lines = majors_file.readlines()
    for line in lines:
        majors.append(line.strip())

## Setup list of terms
terms = []
with open('terms.txt', 'r') as terms_file:
    lines = terms_file.readlines()
    for line in lines:
        terms.append(line.strip())

def parse_course_history():
    """
    Parse course history data from the UNO website and generate JSON output.

    This function parses course history data from the UNO website using BeautifulSoup.
    It collects information about courses, descriptions, prerequisites, and sections.
    The parsed data is then organized into a JSON structure and written to 'course_history.json'.
    """
    # Start parsing...
    courses = {}
    # Loop through each major and each term
    for major in majors:
        for term in terms:
            # Get HTML from website
            print(f"{major} Term {term}", flush=True)
            url = f"https://www.unomaha.edu/registrar/students/before-you-enroll/class-search/index.php?term={term}&session=&subject={major}&catalog_nbr=&career=&instructor=&class_start_time=&class_end_time=&location=&special=&crse_attr_value=&instruction_mode=#anchor-results"
            html = requests.get(url)
            soup = BeautifulSoup(html.content, "html.parser")

            # All courses are "section" elements, loop through them all
            course_elements = soup.find_all("section")
            for course_element in course_elements:
                course_name = course_element["aria-label"]

                # There are two "section" elements that aren't courses, skip them
                if course_name == "UNO Sitewide Links" or course_name == "UNO Contact and Policy Links":
                    continue

                # If a course like this hasn't been parsed yet, create it
                if course_name not in courses:
                    courses[course_name] = {
                        "desc": [],
                        "prereq_text": [],
                        "prereq": [],
                        "sections": []
                    }
                
                # Grab the description and prerequisite text
                text_elements = course_element.find_all("p")
                desc = text_elements[0].get_text().encode('ascii', 'ignore').decode('ascii')
                if len(text_elements) > 1:
                    prereq = text_elements[1].get_text().encode('ascii', 'ignore').decode('ascii')

                # Add the desc and prereq if
                #   1) the course doesn't have any desc/prereq info yet
                #   2) the desc/prereq info has changed since the last term
                if len(courses[course_name]["desc"]) < 1 or desc != courses[course_name]["desc"][-1]:
                    courses[course_name]["desc"].append(desc)
                if len(courses[course_name]["prereq_text"]) < 1 or prereq != courses[course_name]["prereq_text"][-1]:
                    courses[course_name]["prereq_text"].append(prereq)

                # Each course can have several sessions of it during a semester, loop through them all
                sections = course_element.find_all("div",class_="col m-0 mb-4")
                for section in sections:
                    # Get all table rows
                    rows = section.find_all("tr")

                    result = {}
                    
                    for row in rows:
                        h_columns = row.find_all("th")
                        d_columns = row.find_all("td")

                        # Insert header table values into result
                        if len(h_columns) > 1:
                            text1 = h_columns[0].get_text().encode('ascii', 'ignore').decode('ascii')
                            text2 = h_columns[1].get_text().encode('ascii', 'ignore').decode('ascii')
                            result[text1] = text2

                        # Insert body table values into result
                        if len(d_columns) > 1:
                            text1 = d_columns[0].get_text().encode('ascii', 'ignore').decode('ascii')
                            text2 = d_columns[1].get_text().encode('ascii', 'ignore').decode('ascii')
                            if text2 != "Date": # scraper accidentally picks up a weird field, this code make sure it's not inserted
                                result[text1] = text2

                    # Append full result to course sections
                    courses[course_name]["sections"].append(result)

    # Pull prerequisites from text into a separate array 
    for course_name in courses:
        text = courses[course_name]["prereq_text"][-1]
        prereq = re.findall(r"[A-Z]+ [0-9]{3}[0-9A-Z]", text)
        courses[course_name]["prereq"] = prereq

    # Write to JSON file
    with open('course_history.json', 'w') as file:
        file.write(json.dumps(courses, indent=2))

if __name__ == "__main__":
    parse_course_history()
