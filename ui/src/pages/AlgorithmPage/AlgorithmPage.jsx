import "./AlgorithmPage.css";
import TopBar from "../../components/TopBar/TopBar";
import { useState } from 'react';
import courseNames from './course_names.json'; // Import JSON directly
import PredictionTable from "./PredictionTable";

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
    width: '300px',
  };

  const numberSelectStyle = {
    margin: '10px 0',
    padding: '10px',
    borderRadius: '4px',
    border: '1px solid #ccc',
    width: '276px',
  }

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

  const sortedCourseNames = courseNames.sort();

  const [prediction, setPrediction] = useState("");

  const handleChange = (e) => {
    console.log(e.target.name)
    console.log(e.target.value)
    const { name, value } = e.target;
    setFormData(prevState => ({
      ...prevState,
      [name]: value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      if (formData.formType === 'multiple') { // multiple
        const num = parseInt(formData.numberOfCourses);
        if (!num) { return; }
        if (formData.numberOfCourses < 1 || formData.numberOfCourses > 25) { return; }
        const queryString = new URLSearchParams({
          numberOfCourses: formData.numberOfCourses,
          term: 'a',
          year: 'a',
        });
        const result = await fetch(`http://137.48.186.80:8001/run_multi_algorithm?${queryString}`);
        const data = await result.json();
        setPrediction(data.message);
      } else { // single
        const queryString = new URLSearchParams({
          courseId: formData.courseId ? formData.courseId : 'CSCI 1200 CS PRINCIPLES',
          term: 'a',
          year: 'a',
        });
        const result = await fetch(`http://137.48.186.80:8001/run_algorithm?${queryString}`);
        const data = await result.json();
        setPrediction(data.message);
      }
    } catch (e) {
      console.error(e);
    }
  };

  const handleReturn = async (e) => {
    e.preventDefault();
    setFormData(prevState => ({
      ...prevState,
      formType: 'single',
    }));
    setPrediction("");
  };

  return (
    <div className="App" style={containerStyle}>
      <div style={{ padding: '40px' }}></div>
      <TopBar></TopBar>
      {prediction === '' && <form onSubmit={handleSubmit} style={formStyle}>
        <div>Algorithm Run Type</div>
        <div>
          <select name="formType" defaultValue="single" onChange={handleChange}
            style={selectStyle}>
            <option value="single">Collect data on a single course</option>
            <option value="multiple">Select most optimal courses</option>
          </select>
        </div>
        <br></br>
        {formData.formType !== 'multiple' && <div>
          <div>Course ID</div>
          <select
            name="courseId"
            value={formData.courseId}
            onChange={handleChange}
            style={selectStyle}
          >
            {sortedCourseNames.map((course, index) => (
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
            style={numberSelectStyle}
          />
        </div>
        }
        <button type="submit" style={buttonStyle}>
          Submit
        </button>
      </form>
      }
      {prediction !== "" && 
      <div>
      <form onSubmit={handleReturn} style={formStyle}>
        <button type="submit" style={buttonStyle}>
          Return to Algorithm Selection
        </button>
      </form>
      <PredictionTable prediction={prediction}/>
      </div>
      }
    </div>
  );
}

export default AlgorithmPage;
