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

            # These if statements are currently *not* finished. It only assigns Spring courses, and only the season.
            if (("Jan" in data[class_name]['sections'][i]["Date"] or "Feb" in data[class_name]['sections'][i]["Date"]) or 
                ("Mar" in data[class_name]['sections'][i]["Date"] or "Apr" in data[class_name]['sections'][i]["Date"]) or
                ("Jan" in data[class_name]['sections'][i]["Date"] and "May" in data[class_name]['sections'][i]["Date"])):       
                data[class_name]['sections'][i]["Semester"] = "Spring" 
            print(class_name, sections[i])

updated_json = json.dumps(data)
with open('course_convert_dates.json', 'w') as file:
    file.write(updated_json)