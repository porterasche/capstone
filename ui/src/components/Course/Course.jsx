import "./Course.css";
import { Link } from "react-router-dom";

function Course(props) {
  function createLinkElement(courseId) {
    const id = courseId.trim().replace(" ", "");
    const link = `/courses?id=${id}`;

    return <Link key={link} to={link}>{courseId}</Link>;
  }
  
  function stringToElements(str) {
    const coursePattern = /\b[A-Z]{1,4} \d{4}\b/g;
    const matchArray = str.match(coursePattern);
    const descArray = str.split(coursePattern);
    const elements = [];
    elements.push(descArray[0]);
    if (matchArray) {
      matchArray.forEach((match, idx) => {
        elements.push(createLinkElement(match));
        elements.push(descArray[idx+1]);
      });
    }
    return elements;
  }

  // generate element
  const prereqText = props.prereq.length > 0 ? `Prerequisites: ${props.prereq.join(", ")}` : "No Prerequisites.";
  const postreqText = props.postreq.length > 0 ? `Required For: ${props.postreq.join(", ")}` : "";
  return (
    <div className="Course">
      <h2>{stringToElements(props.name)}</h2>
      <p>{stringToElements(props.desc)}</p>
      <p>{stringToElements(prereqText)}</p>
      <p>{stringToElements(postreqText)}</p>
    </div>
  );
}

export default Course;
