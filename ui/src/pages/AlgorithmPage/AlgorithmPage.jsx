import "./AlgorithmPage.css";
import TopBar from "../../components/TopBar/TopBar";
import React, { useState } from 'react';
import CourseList from "../../components/CourseList/CourseList";

function AlgorithmPage() {
  const [formData, setFormData] = useState({
    formType: 'single',
    courseId: '',
    term: '',
    year: '',
    numberOfCourses: 0,
  });

  const [response, setResponse] = useState([]);

  // const [responseMessage, setResponseMessage] = useState('');

  const handleChange = (e) => {
    const { name, value } = e.target;
    console.log(formData)
    setFormData(prevState => ({
      ...prevState,
      [name]: value,
    }));
    console.log(formData)
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log('Data to be sent:', formData);

    if (formData.formType === 'multiple') { // multiple
      const queryString = new URLSearchParams({
        numberOfCourses: formData.numberOfCourses,
        term: formData.term,
        year: formData.year,
      });
      const response = await fetch(`http://137.48.186.80:8001/run_algorithm?${queryString}`);
      const data = await response.json();
    } else { // single
      const queryString = new URLSearchParams({
        courseId: formData.courseId,
        term: formData.term,
        year: formData.year,
      });

    }
    const queryString = new URLSearchParams(formData).toString();

    try {
      // Send GET request to FastAPI server with query parameters
      // LOCAL FETCH
      // const response = await fetch(`http://127.0.0.1:8000/run_algorithm?${queryString}`);
      // DEPLOY FETCH
      const response = await fetch(`http://137.48.186.80:8001/run_algorithm?${queryString}`);
      const data = await response.json();

      const ids = data.map(course => (course.id.toUpperCase()));

      // Handle the response data to update a component, e.g., a message
      setResponse(ids);
      // setResponseMessage(data.message);
      } catch (error) {
      console.error('There was an error!', error);
    }
  };

  const handleReturn = async (e) => {
    e.preventDefault();
    setResponse([]);
  };

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

  const inputStyle = {
    margin: '10px 0',
    padding: '10px',
    borderRadius: '4px',
    border: '1px solid #ccc',
    width: '185px',
  };

  const mainSelectStyle = {
    margin: '10px 0',
    padding: '10px',
    borderRadius: '4px',
    border: '1px solid #ccc',
  }

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

  return (
    <div className="App" style={containerStyle}>
      <TopBar></TopBar>
      { response.length < 1 && <form onSubmit={handleSubmit} style={formStyle}>
        <div>Algorithm Run Type</div>
        <select name="formType" defaultValue="single" onChange={handleChange} 
          style={mainSelectStyle}>
          <option value="single">Collect data on a single course</option>
          <option value="multiple">Select most optimal courses</option>
        </select>
        <br></br>
        { formData.formType !== 'multiple' && <div>
        Course ID (ex: CSCI 3320)
        <input
          type="text"
          name="courseId"
          value={formData.courseId}
          onChange={handleChange}
          placeholder="Course ID"
          style={inputStyle}
        />
        </div>
        }
        { formData.formType === 'multiple' && <div>
        Number of Courses to Select
        <input
          type="number"
          name="numberOfCourses"
          value={formData.numberOfCourses}
          onChange={handleChange}
          placeholder="Number of Courses"
          style={inputStyle}
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
        {response.length > 0 && <div>
        <form onSubmit={handleReturn} style={formStyle}>
        <button type="submit" style={buttonStyle}>
          Rerun Algorithm
        </button>
        </form>
        <CourseList ids={response} style={{ "padding-top": "10px" }} /></div>}
    </div>
  );
}

export default AlgorithmPage;
