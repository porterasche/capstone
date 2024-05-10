/**
 * React component for displaying course information.
 * @component
 */
import "./Course.css";
import { Link } from "react-router-dom";

/**
 * Functional component representing a Course.
 * @param {Object} props - Props passed to the component.
 * @param {string} props.name - Name of the course.
 * @param {string} props.desc - Description of the course.
 * @param {Array<string>} props.prereq - Prerequisites of the course.
 * @param {Array<string>} props.postreq - Courses for which this course is a prerequisite.
 * @returns {JSX.Element} JSX representation of the Course component.
 */
function Course(props) {
  /**
   * Function to create a Link element for a course ID.
   * @param {string} courseId - ID of the course.
   * @returns {JSX.Element} Link element for the course ID.
   */
  function createLinkElement(courseId) {
    const id = courseId.trim().replace(" ", "");
    const link = `/courses?id=${id}`;

    return <Link key={link} to={link} style={{ color:'#282cBB' }}>{courseId}</Link>;
  }
  
  /**
   * Function to convert a string containing course IDs into an array of elements with links.
   * @param {string} str - String containing course IDs and descriptions.
   * @returns {Array<JSX.Element>} Array of elements with links.
   */
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

  // Generate elements for course information
  const prereqText = props.prereq.length > 0 ? `Prerequisites: ${props.prereq.join(", ")}` : "No Prerequisites.";
  const postreqText = props.postreq.length > 0 ? `Required For: ${props.postreq.join(", ")}` : "";

  let desc = props.desc;
  if (desc.length > 480) {
    desc = desc.substring(0, 480);
    desc += '...';
  }

  return (
    <div className="Course">
      <h2>{stringToElements(props.name)}</h2>
      <p>{stringToElements(desc)}</p>
      <p>{stringToElements(prereqText)}</p>
      <p>{stringToElements(postreqText)}</p>
    </div>
  );
}

export default Course;
