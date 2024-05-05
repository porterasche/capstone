## @package webscraper
#  Documentation for this module.
#
#  The purpose of this file is to take the .json file that course_history.py,
#  look at the dates for each section for all of the courses, and then
#  generate a new "Semester" parameter that for each of those sections.
#  For example, if a section has a date of "Aug 21, 2023 - Dec 15, 2023",
#  then it is given a semester of "Fall 2023". 
#  This updated information is then written to course_convert_dates.json.

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

# Setup list of majors
import json

def process_json_data():
    """
    Process JSON data to generate 'Semester' parameter for each section.

    This function processes JSON data read from 'course_history.json'. It looks
    at the dates for each section and calculates the corresponding semester. The
    updated information with the 'Semester' parameter is then written to
    'course_convert_dates.json'.

    Returns:
        dict: Updated JSON data with 'Semester' parameter for each section.
    """
    # Open the course_history.json file to read.
    with open('course_history.json') as f:
        data = json.load(f)

        for class_name in data:
            sections = data[class_name]['sections']
            for i in range(len(sections)):
                # Look through data[class_name]['sections'][i]["Semester"] and calculate whether it is
                # Spring (Winter sessions count as Spring according to terms), Summer, or Fall.
                if ("Jan" in sections[i]["Date"] or "Feb" in sections[i]["Date"] or 
                    "Mar" in sections[i]["Date"] or "Apr" in sections[i]["Date"] or
                    ("Jan" in sections[i]["Date"] and "May" in sections[i]["Date"])):       
                    sections[i]["Semester"] = ""
                    # Can't combine a str and a list together, so we make two temp strings to mash together.
                    # Also, using a regular expression to find the year.
                    temp = "Spring"
                    temp2 = ''.join(re.findall(r"([0-9]{4}) ", sections[i]["Date"]))
                    sections[i]["Semester"] = ' '.join((temp, temp2))

                elif ("May" in sections[i]["Date"] or "Jun" in sections[i]["Date"] or 
                    "Jul" in sections[i]["Date"] or
                    ("May" in sections[i]["Date"] and "Aug" in sections[i]["Date"])):       
                    sections[i]["Semester"] = ""
                    # Can't combine a str and a list together, so we make two temp strings to mash together.
                    # Also, using a regular expression to find the year.
                    temp = "Summer"
                    temp2 = ''.join(re.findall(r"([0-9]{4}) ", sections[i]["Date"]))
                    sections[i]["Semester"] = ' '.join((temp, temp2))

                elif ("Aug" in sections[i]["Date"] or "Sep" in sections[i]["Date"] or 
                    "Oct" in sections[i]["Date"] or "Nov" in sections[i]["Date"] or
                    ("Aug" in sections[i]["Date"] and "Dec" in sections[i]["Date"])):       
                    sections[i]["Semester"] = ""
                    # Can't combine a str and a list together, so we make two temp strings to mash together.
                    # Also, using a regular expression to find the year.
                    temp = "Fall"
                    temp2 = ''.join(re.findall(r"([0-9]{4}) ", sections[i]["Date"]))
                    sections[i]["Semester"] = ' '.join((temp, temp2))

                else:
                    sections[i]["Semester"] = "ERROR! Likely culprit is course_convert_dates.py!"

                print(class_name, sections[i])

    # Write to a new file named course_convert_dates.json that has the newly generated "Semester" parameters.
    with open('course_convert_dates.json', 'w') as file:
        file.write(json.dumps(data, indent=2))

    return data

if __name__ == "__main__":
    process_json_data()
