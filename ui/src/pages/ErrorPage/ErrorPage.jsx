/**
 * React component for the Error Page.
 * This component displays an error message when a page is not found.
 * @component
 */
import "./ErrorPage.css";
import TopBar from "../../components/TopBar/TopBar";

/**
 * Functional component representing the Error Page.
 * @returns {JSX.Element} JSX representation of the Error Page.
 */
function ErrorPage() {
  return (
    <div className="App">
      <TopBar></TopBar>
      <div>Error: Page not Found</div>
    </div>
  );
}

export default ErrorPage;
