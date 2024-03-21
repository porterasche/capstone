import "./CoursePage.css";
import CourseList from "../../components/CourseList/CourseList";
import TopBar from "../../components/TopBar/TopBar";

function CoursePage() {
  return (
    <div className="App">
      <TopBar></TopBar>
      <div>
        <CourseList style={{ "padding-top": "10px" }} />
      </div>
    </div>
  );
}

export default CoursePage;
