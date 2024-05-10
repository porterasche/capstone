import "./CoursePage.css";
import CourseList from "../../components/CourseList/CourseList";
import TopBar from "../../components/TopBar/TopBar";
import { useSearchParams } from 'react-router-dom';

function CoursePage() {
  const [searchParams, setSearchParams] = useSearchParams();
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
