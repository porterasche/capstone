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

courses = []
for major in majors:
    major_url = f"https://catalog.unomaha.edu/undergraduate/coursesaz/{major.lower()}/"
    major_html = requests.get(major_url)
    major_soup = BeautifulSoup(major_html.content, "html.parser")

    courseblock_elements = major_soup.find_all("div", class_="courseblock")


    for courseblock in courseblock_elements:
        title = courseblock.findChildren("p",class_="courseblocktitle noindent")[0].get_text().encode('ascii', 'ignore').decode('ascii')
        desc = courseblock.findChildren("p",class_="courseblockdesc noindent")[0].get_text().encode('ascii', 'ignore').decode('ascii')

        courses.append({
            'title': title,
            'desc': desc.strip().split("\n")
        })
    print(f"{major}: {len(courses)} courses", flush=True)



# Title formatted like CSCI1200COURSE NAME (3 credits)
# Desc has up to 3 elements (desc, prereqs, misc)
results = []
for course in courses:
    id = re.search(r"[A-Z]+[0-9]+", course['title']).group()
    name = course['title'][(len(id)):]
    desc = course['desc'][0]
    prereqs = ""
    misc = ""

    if len(course['desc']) > 1:
        prereqs = course['desc'][1]

    if len(course['desc']) > 2:
        misc = course['desc'][2]

    results.append({
        'id': id,
        'name': name,
        'desc': desc,
        'prereqs': prereqs,
        'misc': misc
    })

with open('courses.json', 'w') as file:
    file.write(json.dumps(results, indent=2))
