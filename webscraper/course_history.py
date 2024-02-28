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

majors = []
with open('majors.txt', 'r') as majors_file:
    lines = majors_file.readlines()
    for line in lines:
        majors.append(line.strip())

terms = []
with open('terms.txt', 'r') as terms_file:
    lines = terms_file.readlines()
    for line in lines:
        terms.append(line.strip())

courses = {}
for major in majors:
    for term in terms:
        print(f"MAJOR{major} - TERM{term}", flush=True)
        url = f"https://www.unomaha.edu/registrar/students/before-you-enroll/class-search/index.php?term={term}&session=&subject={major}&catalog_nbr=&career=&instructor=&class_start_time=&class_end_time=&location=&special=&crse_attr_value=&instruction_mode=#anchor-results"
        html = requests.get(url)
        soup = BeautifulSoup(html.content, "html.parser")

        course_elements = soup.find_all("section")

        for course_element in course_elements:
            course_name = course_element["aria-label"]
            if course_name == "UNO Sitewide Links" or course_name == "UNO Contact and Policy Links":
                continue
            print(f"{course_name}", flush=True)
            if course_name not in courses:
                courses[course_name] = {
                    'sections': []
                }

            sections = course_element.findChildren("div",class_="col m-0 mb-4")
            for section in sections:
                head_rows = section.find("thead").findChildren("tr")
                body_rows = section.findChildren("tr")

                result = {}
                
                for row in head_rows:
                    columns = row.find_all("th")
                    text1 = columns[0].get_text().encode('ascii', 'ignore').decode('ascii')
                    text2 = columns[1].get_text().encode('ascii', 'ignore').decode('ascii')
                    result[text1] = text2

                for row in body_rows:
                    columns = row.findChildren("td")
                    if len(columns) < 2:
                        continue
                    text1 = columns[0].get_text().encode('ascii', 'ignore').decode('ascii')
                    text2 = columns[1].get_text().encode('ascii', 'ignore').decode('ascii')
                    if text2 != "Date":
                        result[text1] = text2
            
            courses[course_name]["sections"].append(result)



# Title formatted like CSCI1200COURSE NAME (3 credits)
# Desc has up to 3 elements (desc, prereqs, misc)

with open('course_history.json', 'w') as file:
    file.write(json.dumps(courses, indent=2))
