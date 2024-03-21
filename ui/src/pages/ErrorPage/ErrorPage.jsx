import "./ErrorPage.css";
import TopBar from "../../components/TopBar/TopBar";

function ErrorPage() {
  return (
    <div className="App">
      <TopBar></TopBar>
      <div>
        Error: Page not Found
      </div>
    </div>
  );
}

export default ErrorPage;
