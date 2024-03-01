import './App.css';
import CourseList from './components/CourseList/CourseList';

function App() {

  return (
    <div className="App">
      <header className="App-header">
        <a
          className="App-link"
          href="https://www.unomaha.edu/registrar/students/before-you-enroll/class-search/index.php"
          target="_blank"
          rel="noopener noreferrer"
        >
          Data Scraped from Course Registrar
        </a>
      </header>
      <div>
        <CourseList/>
      </div>
    </div>
  );
}

export default App;
