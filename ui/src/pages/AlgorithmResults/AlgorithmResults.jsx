/**
 * React component for the Course Page.
 * This component displays a list of courses.
 * @component
 */
import "./CoursePage.css";
import CourseList from "../../components/CourseList/CourseList";
import TopBar from "../../components/TopBar/TopBar";

/**
 * Functional component representing the Course Page.
 * @returns {JSX.Element} JSX representation of the Course Page.
 */
function CoursePage() {
  return (
    <div>
      <TopBar></TopBar>
      <div>
        <CourseList style={{ "padding-top": "10px" }} />
      </div>
    </div>
  );
}

export default CoursePage;
