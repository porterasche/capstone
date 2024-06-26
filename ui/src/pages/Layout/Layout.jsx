/**
 * React component for the Layout.
 * This component defines the layout structure of the application.
 * @component
 */
import "./Layout.css";
import { AppBar, Box, Container } from "@mui/material";
import { Link } from "react-router-dom";

/**
 * Functional component representing the Layout.
 * @returns {JSX.Element} JSX representation of the Layout.
 */
function Layout() {
  return (
    <div className="App">
      <AppBar className="App-header">
        <Container maxWidth="xl">
          <Box sx={{ flexGrow: 0 }}>
            <Link to="/algorithm">algorithms</Link>
            <a
              className="App-link"
              href="https://www.unomaha.edu/registrar/students/before-you-enroll/class-search/index.php"
              target="_blank"
              rel="noopener noreferrer"
            >
              Course Listing
            </a>
          </Box>
          <Box sx={{ flexGrow: 0 }}>
            <a
              className="App-link"
              href="https://www.unomaha.edu/registrar/students/before-you-enroll/class-search/index.php"
              target="_blank"
              rel="noopener noreferrer"
            >
              Algorithm
            </a>
          </Box>
        </Container>
      </AppBar>
    </div>
  );
}

export default Layout;
