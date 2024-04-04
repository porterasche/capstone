import "./AlgorithmPage.css";
import TopBar from "../../components/TopBar/TopBar";
import React, { useState } from 'react';
import CourseList from "../../components/CourseList/CourseList";

function AlgorithmPage() {
  const [formData, setFormData] = useState({
    field1: '',
    field2: '',
    field3: '',
  });

  const [response, setResponse] = useState([]);

  // const [responseMessage, setResponseMessage] = useState('');

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

    const queryString = new URLSearchParams(formData).toString();

    try {
      // Send GET request to FastAPI server with query parameters
      const response = await fetch(`http://127.0.0.1:8000/run_algorithm?${queryString}`);
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
  }

  const formStyle = {
    display: 'flex',
    flexDirection: 'column',
    width: '300px',
    margin: '50px auto',
    padding: '20px',
    borderRadius: '8px',
    backgroundColor: 'white',
    boxShadow: '0 4px 10px rgba(0, 0, 0, 0.1)',
  };

  const inputStyle = {
    margin: '10px 0',
    padding: '10px',
    borderRadius: '4px',
    border: '1px solid #ccc',
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
        <input
          type="text"
          name="field1"
          value={formData.field1}
          onChange={handleChange}
          placeholder="Field 1"
          style={inputStyle}
        />
        <input
          type="text"
          name="field2"
          value={formData.field2}
          onChange={handleChange}
          placeholder="Field 2"
          style={inputStyle}
        />
        <input
          type="text"
          name="field3"
          value={formData.field3}
          onChange={handleChange}
          placeholder="Field 3"
          style={inputStyle}
        />
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
