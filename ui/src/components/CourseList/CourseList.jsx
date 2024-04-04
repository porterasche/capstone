import { courseData } from "./courseData";
import Course from "../Course/Course";
import { useSearchParams } from 'react-router-dom';

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
  const elements = arr.map((course) => ( // TODO - switch key to course.id
    <Course name={course.name} key={course.name} desc={course.desc} prereq={course.prereq} postreq={course.postreq}/>
  ));

  return elements;
}

function CourseList() {
  const [searchParams, setSearchParams] = useSearchParams();
  const id = searchParams.get('id');

  let data = getCourseData();

  data = data.filter(course => !id || (course.id.includes(id)));

  if (data.length < 1) {
    let onlyCSCI = "";
    if (!id.startsWith("CSCI")) {
      onlyCSCI = " Only CSCI courses are available to be searched at this time.";
    }
    return <p>No courses found for {id}.{onlyCSCI}</p>
  }

  return <div className="CourseList">{getCourseElements(data)}</div>;
}

export default CourseList;
