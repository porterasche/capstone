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

## Documentation

The generated documentation for the project can be found at this link for the python backend files: [Documentation](https://porterasche.github.io/capstone/files.html). The generated documentation for the front end can be found at this link:

## Release Notes

### Code Milestone 1

-   Added 2 initial webscraper scripts to gather data from UNO's websites
-   Created a script to clean up the webscraped data to make it easier for us to use
-   Created a React UI that displays all CSCI course information


### Code Milestone 2 
-   Added the prototype algorithm, one algorithm prediction for the following year and one for calculating the accuracy of a prediction
-   Created a CRON job to pull and push changes automatically
-   Created a script that will be ran by the CRON Job to automatically restart the UI with current changes
-   Updated UI to include multiple routes for different tabs (Course Listing, Algorithm, Prerequisite Viewer, Course Registrar)

### Code Milestone 3
-   Added links to prerequisites and required courses under each course, and the ability to select (or jump) to that course
-   Created a mock algorithm user interface to input parameters into the algorithm function in backend.
-   Set up a FastAPI server to connect the UI with the backend, and send responses bidirectionally.
-   Fixed the data so it can be better interacted with the algorithm, and replaced dates with the terms, and a more accurate prediction.
-   Parameterized the algorithm so it can be called as a function and passed in parameters.
-   Converted dates in courses into more readable semester format, and stored them.

### Code Milestone 4
-   Updated UI to display prediction algorithm results.
-   Updated UI to allow selection of course to predict.
-   Setup new endpoints for the algorithm results in UI
-   Added Pre-req viewer using cytoscape
-   Increase pediction algorithm testing accuracy function
-   Improved progress on Algorithm using prereqs.
