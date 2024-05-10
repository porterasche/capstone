/**
 * React component for the Course Page.
 * This component displays a list of courses based on search parameters.
 * @component
 */
import "./CoursePage.css";
import CourseList from "../../components/CourseList/CourseList";
import TopBar from "../../components/TopBar/TopBar";
import { useSearchParams } from 'react-router-dom';

/**
 * Functional component representing the Course Page.
 * @returns {JSX.Element} JSX representation of the Course Page.
 */
function CoursePage() {
  /**
   * Hook to access and update search parameters in the URL.
   * @type {Function}
   */
  const [searchParams, setSearchParams] = useSearchParams();

  /**
   * Array containing course IDs extracted from search parameters.
   * @type {Array<string>}
   */
  const ids = [];
  if (searchParams.get('id')) {
    ids.push(searchParams.get('id'));
  }

  return (
    <div>
      <TopBar></TopBar>
      <div style={{ padding: '40px' }}></div>
      <div>
        <CourseList ids={ids} style={{ "padding-top": "10px" }} />
      </div>
    </div>
  );
}

export default CoursePage;
