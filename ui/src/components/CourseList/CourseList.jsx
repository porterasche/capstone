import { courseData } from "./courseData";
import Course from "../Course/Course";

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

function getCourseElements(arr) {
  const elements = arr.map((course) => ( // switch key to course.id when all duplicates are removed
    <Course key={course.id} name={course.name} desc={course.desc} prereq={course.prereq} postreq={course.postreq}/>
  ));

  return elements;
}

function CourseList(props) {
  let data = getCourseData();

  if (props.ids && props.ids.length > 0) {
    data = data.filter(course => (props.ids.includes(course.id)));
  }

  if (data.length < 1) {
    return <p>No courses found. (Only CSCI courses are available to be searched at this time.)</p>
  }

  return <div className="CourseList">{getCourseElements(data)}</div>;
}

export default CourseList;
