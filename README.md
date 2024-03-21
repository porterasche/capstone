# Course Planning Selection Algorithm

Capstone Group 7 (Porter Asche, Jacob Rohrich, Nathan Perkins, Nathan Stone)

This project currently consists of a **Python Webscraper** (to collect course data from the University of Nebraska-Omaha's website), a **React UI** (hosted at http://137.48.186.80/), and a **Django Server**.

We have a [Trello Board](https://trello.com/b/EQg635eu/csci4970-capstone-project) documenting our progress on current tickets.

## Python Webscraper

To setup the webscraper, first download the latest version of [Python](https://www.python.org/downloads/). Open a terminal in the `capstone/webscraper` directory. Then, download the required packages with the commands `python -m pip install requests` and `python -m pip install beautifulsoup4`.

There are several webscraper scripts, and each can be ran with `python <script_name.py>`. The current existing scripts are listed below...

| File Name            | Description                                                                                                        | Output                 |
| -------------------- | ------------------------------------------------------------------------------------------------------------------ | ---------------------- |
| `course_listing.py`  | Pulls basic course descriptions and prerequisite listings from https://catalog.unomaha.edu/undergraduate/coursesaz | `courses.json`         |
| `cleanup_prereqs.py` | Uses the data from `courses.json` to clean the prerequisite text into a simple array                               | `cleaned_courses.json` |
| `course_history.py`  | Gets historical course data from each session from Spring 2019 to Fall 2024                                        | `course_history.json`  |

## React UI

To run the React UI, you need the latest version of [Node.js](https://nodejs.org/en/download/). Open a terminal in the `capstone/ui` directory and run `npm start` to host the UI locally at http://localhost:3000/. To build for deployment, run `npm run build` and the application will be built in `capstone/ui/build`.

## Django Server

You will also need Python for the server, along with the additional package that can be downloaded with `python -m pip install Django`. Open a terminal in `capstone/server` and start it by running the command `python manage.py runserver`. You can visit http://localhost:8000/courses/ to see the basic homepage. Documentation for continuing to set up this server can be found at https://docs.djangoproject.com/en/5.0/intro/tutorial01/.

## Release Notes

### Code Milestone 1

-   Added 2 initial webscraper scripts to gather data from UNO's websites
-   Created a script to clean up the webscraped data to make it easier for us to use
-   Created a React UI that displays all CSCI course information
