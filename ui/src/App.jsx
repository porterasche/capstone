import "./App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import CoursePage from "./pages/CoursesPage/CoursePage";
import AlgorithmPage from "./pages/AlgorithmPage/AlgorithmPage";
import ErrorPage from "./pages/ErrorPage/ErrorPage";
import PrereqPage from "./pages/PrereqPage/PrereqPage";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<CoursePage />} />
        <Route path="courses" element={<CoursePage />} />
        <Route path="algorithm" element={<AlgorithmPage />} />
        <Route path="prereqs" element={<PrereqPage />} />
        <Route path="*" element={<ErrorPage />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
