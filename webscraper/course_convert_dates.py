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

with open('course_history.json') as f:
    data = json.load(f)

    for class_name in data:
        sections = data[class_name]['sections']
        for i in range(len(sections)):

            # Look through data[class_name]['sections'][i]["Semester"] and calculate whether it is
            # Spring (Winter sessions count as Spring according to terms), Summer, or Fall.
            if ("Jan" in data[class_name]['sections'][i]["Date"] or "Feb" in data[class_name]['sections'][i]["Date"] or 
                "Mar" in data[class_name]['sections'][i]["Date"] or "Apr" in data[class_name]['sections'][i]["Date"] or
                ("Jan" in data[class_name]['sections'][i]["Date"] and "May" in data[class_name]['sections'][i]["Date"])):       
                data[class_name]['sections'][i]["Semester"] = ""
                # Can't combine a str and a list together, so we make two temp strings to mash together.
                # Also, using a regular expression to find the year.
                temp = "Spring"
                temp2 = ''.join(re.findall(r"([0-9]{4}) ", data[class_name]['sections'][i]["Date"]))
                data[class_name]['sections'][i]["Semester"] = ' '.join((temp, temp2))

            elif ("May" in data[class_name]['sections'][i]["Date"] or "Jun" in data[class_name]['sections'][i]["Date"] or 
                "Jul" in data[class_name]['sections'][i]["Date"] or
                ("May" in data[class_name]['sections'][i]["Date"] and "Aug" in data[class_name]['sections'][i]["Date"])):       
                data[class_name]['sections'][i]["Semester"] = ""
                # Can't combine a str and a list together, so we make two temp strings to mash together.
                # Also, using a regular expression to find the year.
                temp = "Summer"
                temp2 = ''.join(re.findall(r"([0-9]{4}) ", data[class_name]['sections'][i]["Date"]))
                data[class_name]['sections'][i]["Semester"] = ' '.join((temp, temp2))

            elif ("Aug" in data[class_name]['sections'][i]["Date"] or "Sep" in data[class_name]['sections'][i]["Date"] or 
                "Oct" in data[class_name]['sections'][i]["Date"] or "Nov" in data[class_name]['sections'][i]["Date"] or
                ("Aug" in data[class_name]['sections'][i]["Date"] and "Dec" in data[class_name]['sections'][i]["Date"])):       
                data[class_name]['sections'][i]["Semester"] = ""
                # Can't combine a str and a list together, so we make two temp strings to mash together.
                # Also, using a regular expression to find the year.
                temp = "Fall"
                temp2 = ''.join(re.findall(r"([0-9]{4}) ", data[class_name]['sections'][i]["Date"]))
                data[class_name]['sections'][i]["Semester"] = ' '.join((temp, temp2))

            else:
                data[class_name]['sections'][i]["Semester"] = "ERROR! Likely culprit is course_convert_dates.py!"

            print(class_name, sections[i])

# Then, write to course_convert_dates.json
with open('course_convert_dates.json', 'w') as file:
    file.write(json.dumps(data, indent=2))
