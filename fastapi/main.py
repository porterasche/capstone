from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from algorithm.PredicitionAlgo import predict_enrollment, read_json_data
import json

app = FastAPI()
# pip install fastapi[all]

app.add_middleware(
    CORSMiddleware, # SHOULD SPECIFY EXACT ORIGIN FOR PROPER SECURITY
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/process")
async def process(field1: str = Query(None), field2: str = Query(None), field3: str = Query(None)):
    """
    Process data from query parameters.

    This endpoint processes data received from query parameters.
    It performs some work based on the received values and returns a message.

    Args:
        field1 (str): The value of field1.
        field2 (str): The value of field2.
        field3 (str): The value of field3.

    Returns:
        dict: A dictionary containing a message with the processed data.
    """
    # Do some work with the received values
    result = "Result From FastAPI Server"

    # Send a response back to the UI
    return {"message": f"Processed: field1={field1}, field2={field2}, field3={field3}, result={result}"}

@app.get("/run_algorithm")
async def run_algorithm(courseId: str, term: str = Query(None), year: str = Query(None)):
    """
    Run enrollment prediction algorithm for a course.

    This endpoint runs an enrollment prediction algorithm for a specific course.
    It returns the predicted enrollment for the specified course and term.

    Args:
        courseId (str): The ID of the course.
        term (str, optional): The term for which to predict enrollment. Defaults to None.
        year (str, optional): The year for which to predict enrollment. Defaults to None.

    Returns:
        dict: A dictionary containing a message with the predicted enrollment.
    """
    # return list of 3 classes
    data_file_path = "../data_alteration/summarized_course_data.json"
    course_data = read_json_data(data_file_path)
    future_term, predicted_enrollment = predict_enrollment(course_data, courseId)
    return {"message": f"Predicted enrollment for {courseId} in {future_term}: {predicted_enrollment}"}

@app.get("/run_multi_algorithm")
async def run_multi_algorithm(numberOfCourses: int, term: str = Query(None), year: str = Query(None)):
    """
    Run enrollment prediction algorithm for multiple courses.

    This endpoint runs an enrollment prediction algorithm for multiple courses.
    It returns the predicted enrollment for the specified number of courses.

    Args:
        numberOfCourses (int): The number of courses for which to predict enrollment.
        term (str, optional): The term for which to predict enrollment. Defaults to None.
        year (str, optional): The year for which to predict enrollment. Defaults to None.

    Returns:
        dict: A dictionary containing a message with the predicted enrollment for multiple courses.
    """
    # return list of 3 classes
    data_file_path = "../data_alteration/summarized_course_data.json"
    resultString = ""
    data = []
    course_data = read_json_data(data_file_path)
    count = numberOfCourses
    with open('course_names.json', 'r') as file:
        courses = json.load(file)
    for courseId in courses:
        future_term, predicted_enrollment = predict_enrollment(course_data, courseId)
        data.append({'key': predicted_enrollment, 'value': courseId})
    sortedCourses = sorted(data, key=lambda x: x['key'])
    for i in range(numberOfCourses):
        resultString += f"(Predicted enrollment for {sortedCourses[sortedCourses.__len__()-1-i]['value']}: {sortedCourses[sortedCourses.__len__()-1-i]['key']}) "
    return {"message": resultString}
