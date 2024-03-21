import { courseData } from './courseData';
import Course from '../Course/Course';

const getCourseElements = () => {
    const arr = [];
    for (const key in courseData) {
        arr.push({
            name: key,
            desc: courseData[key].desc,
            prereq: courseData[key].prereq.length > 0 ? `Prerequisites: ${courseData[key].prereq.join(', ')}` : 'No Prerequisites.'
        });
    }

    const elements = arr.map(course => (<Course name={course.name} desc={course.desc} prereq={course.prereq}/>))

    return elements;
}

function CourseList() {

  return (
    <div className="CourseList">
        {getCourseElements()}
    </div>
  );
}

export default CourseList;
