import "./TopBar.css";
import { Link } from "react-router-dom";
import AppBar from "@mui/material/AppBar";
import Box from "@mui/material/Box";
import Toolbar from "@mui/material/Toolbar";
import Button from "@mui/material/Button";
import ViewListIcon from "@mui/icons-material/ViewList";
import SettingsSuggestIcon from "@mui/icons-material/SettingsSuggest";
import MenuBookIcon from "@mui/icons-material/MenuBook";
import AccountTreeIcon from "@mui/icons-material/AccountTree";

export default function TopBar() {
  return (
    <>
      <Box sx={{ flexGrow: 1 }}>
        <AppBar>
          <Toolbar className="TopBar-main">
            <Link to="/courses" className="TopBar-text">
              <Button color="inherit">
                <ViewListIcon className="TopBar-icon" />
                Course Listing
              </Button>
            </Link>
            <Link to="/algorithm" className="TopBar-text">
              <Button color="inherit">
                <SettingsSuggestIcon className="TopBar-icon" />
                Algorithm
              </Button>
            </Link>
            <Link to="/prereqs" className="TopBar-text">
              <Button color="inherit">
                <AccountTreeIcon className="TopBar-icon" />
                Prerequisite Viewer
              </Button>
            </Link>
            <a
              href="https://www.unomaha.edu/registrar/students/before-you-enroll/class-search/index.php"
              target="_blank"
              rel="noopener noreferrer"
              className="TopBar-text"
            >
              <Button color="inherit">
                <MenuBookIcon />
                Course Registrar
              </Button>
            </a>
          </Toolbar>
        </AppBar>
      </Box>
      <div className="TopBar-padding"></div>
    </>
  );
}
