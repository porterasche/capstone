import "./Course.css";

function Course(props) {
  return (
    <div className="Course">
      <h2>{props.name}</h2>
      <p>{props.desc}</p>
      <p>{props.prereq}</p>
    </div>
  );
}

export default Course;
