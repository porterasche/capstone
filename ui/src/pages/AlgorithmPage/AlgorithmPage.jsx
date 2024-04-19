import "./AlgorithmPage.css";
import TopBar from "../../components/TopBar/TopBar";
import { useState, useEffect } from 'react';
import CourseList from "../../components/CourseList/CourseList";
import courseNames from './course_names.json'; // Import JSON directly

function AlgorithmPage() {
  const formStyle = {
    display: 'flex',
    flexDirection: 'column',
    width: '300px',
    margin: '50px auto',
    padding: '20px',
    borderRadius: '8px',
    backgroundColor: 'white',
    boxShadow: '0 4px 10px rgba(0, 0, 0, 0.1)',
    justifyContent: 'center',
  };

  const selectStyle = {
    margin: '10px 0',
    padding: '10px',
    borderRadius: '4px',
    border: '1px solid #ccc',
    width: '200px',
  };

  const buttonStyle = {
    padding: '10px 20px',
    border: 'none',
    borderRadius: '4px',
    backgroundColor: '#007BFF',
    color: 'white',
    cursor: 'pointer',
    marginTop: '10px',
  };

  const containerStyle = {
    display: 'auto',
    alignItems: 'center',
    justifyContent: 'center',
    height: '100vh',
    background: 'linear-gradient(135deg, #89f7fe 0%, #66a6ff 100%)',
  };

  const [formData, setFormData] = useState({
    formType: 'single',
    courseId: '',
    term: '',
    year: '',
    numberOfCourses: 0,
  });

  const [response, setResponse] = useState({
    formType: 'none',
    data: {},
  });

  const [prediction, setPrediction] = useState("");

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prevState => ({
      ...prevState,
      [name]: value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log('Data to be sent:', formData);

    try {
      if (formData.formType === 'multiple') { // multiple
        const queryString = new URLSearchParams({
          numberOfCourses: formData.numberOfCourses,
          term: formData.term,
          year: formData.year,
        });
        const result = await fetch(`http://137.48.186.80:8001/run_multi_algorithm?${queryString}`);
        const data = await result.json();
        setPrediction(data.message);
        const ids = data.map(course => (course.id.toUpperCase()));
        setResponse({
          type: 'single',
          data: ids,
        });
      } else { // single
        const queryString = new URLSearchParams({
          courseId: formData.courseId,
          term: formData.term,
          year: formData.year,
        });
        const result = await fetch(`http://137.48.186.80:8001/run_algorithm?${queryString}`);
        const data = await result.json();
        setPrediction(data.message);
        setResponse({
          type: 'single',
          data: data,
        });
      }
    } catch (e) {
      console.error(e);
    }
  };

  const handleReturn = async (e) => {
    e.preventDefault();
    setResponse({
      formType: 'none',
      data: {},
    });
    setPrediction("");
  };

  let algoResults = null;
  if (response.formType === 'multiple') {
    algoResults = (
      <div>
        <form onSubmit={handleReturn} style={formStyle}>
          <button type="submit" style={buttonStyle}>
            Return to Algorithm Selection
          </button>
        </form>
        <CourseList ids={response} style={{ "padding-top": "10px" }} />
      </div>
    );
  } else if (response.formType === 'single') {
    algoResults = (
      <div>
        Single results response here!
      </div>
    )
  }

  return (
    <div className="App" style={containerStyle}>
      <TopBar></TopBar>
      {response.formType === 'none' && <form onSubmit={handleSubmit} style={formStyle}>
        <div>Algorithm Run Type</div>
        <select name="formType" defaultValue="single" onChange={handleChange}
          style={selectStyle}>
          <option value="single">Collect data on a single course</option>
          <option value="multiple">Select most optimal courses</option>
        </select>
        <br></br>
        {formData.formType !== 'multiple' && <div>
          <div>Course ID</div>
          <select
            name="courseId"
            value={formData.courseId}
            onChange={handleChange}
            style={selectStyle}
          >
            {courseNames.map((course, index) => (
              <option key={index} value={course}>{course}</option>
            ))}
          </select>
        </div>
        }
        {formData.formType === 'multiple' && <div>
          Number of Courses to Select
          <input
            type="number"
            name="numberOfCourses"
            value={formData.numberOfCourses}
            onChange={handleChange}
            placeholder="Number of Courses"
            style={selectStyle}
          />
        </div>
        }
        <div>
          <div>Term</div>
          <select name="term" defaultValue="fall" onChange={handleChange} style={selectStyle}>
            <option value="fall">Fall</option>
            <option value="spring">Spring</option>
          </select>
          <div>Year</div>
          <select name="year" defaultValue="2023" onChange={handleChange} style={selectStyle}>
            <option value="2019">2019</option>
            <option value="2020">2020</option>
            <option value="2021">2021</option>
            <option value="2022">2022</option>
            <option value="2023">2023</option>
            <option value="2024">2024</option>
          </select>
        </div>
        <button type="submit" style={buttonStyle}>
          Submit
        </button>
      </form>}
      {prediction != "" && 
      <div>
      <form onSubmit={handleReturn} style={formStyle}>
        <button type="submit" style={buttonStyle}>
          Return to Algorithm Selection
        </button>
      </form>
      <p>{prediction}</p>
      </div>
      }
    </div>
  );
}

export default AlgorithmPage;
