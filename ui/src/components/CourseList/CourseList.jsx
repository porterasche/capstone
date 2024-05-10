/**
 * React component for the Course List.
 * This component displays a list of courses.
 * @component
 */
import { courseData } from "./courseData";
import Course from "../Course/Course";

/**
 * Function to retrieve course data from courseData object.
 * @returns {Array<Object>} Array containing course data objects.
 */
function getCourseData() {
  const arr = [];
  for (const key in courseData) {
    const id = key.match(/\b[A-Z]{1,4} \d{4}\b/g)[0];
    const postreqs = [];
    for (const postreqKey in courseData) {
      if (courseData[postreqKey].prereq.includes(id)) {
        postreqs.push(postreqKey.match(/\b[A-Z]{1,4} \d{4}\b/g)[0]);
      }
    }
    arr.push({
      id: id.replace(" ", ""),
      name: key,
      desc: courseData[key].desc[courseData[key].desc.length - 1],
      prereq:
        courseData[key].prereq,
      postreq: postreqs,
    });
  }

  return arr;
}

/**
 * Function to generate Course elements from course data.
 * @param {Array<Object>} arr - Array containing course data objects.
 * @returns {Array<JSX.Element>} Array of Course elements.
 */
function getCourseElements(arr) {
  const elements = arr.map((course) => (
    <Course key={course.id} name={course.name} desc={course.desc} prereq={course.prereq} postreq={course.postreq}/>
  ));

  return elements;
}

/**
 * Functional component representing the Course List.
 * @param {Object} props - Props passed to the component.
 * @param {Array<string>} [props.ids] - IDs of courses to be displayed.
 * @returns {JSX.Element} JSX representation of the Course List.
 */
function CourseList(props) {
  let data = getCourseData();

  if (props.ids && props.ids.length > 0) {
    data = data.filter(course => (props.ids.includes(course.id)));
  }

  if (data.length < 1) {
    return <p style={{ padding: '20px' }}>
      No courses found. (Only CSCI courses are available to be searched)
    </p>
  }

  data = data.sort((a,b) => {
    if (a.name < b.name) {
      return - 1;
    }
    return 1;
  });

  return <div className="CourseList">{getCourseElements(data)}</div>;
}

export default CourseList;
