import axios from "axios";
import { Link, Route, Routes } from "react-router-dom";
import LogIn from "./pages/LogIn";
import SignUp from "./pages/SignUp";

const App = () => {
  // test route
  axios.get("/api/user/test").then((result) => {
    console.log(result.data.message);
  });

  return (
    <>
      <p>
        <Link to="/login">Log In</Link>
        {" | "}
        <Link to="/signup">Sign Up</Link>
      </p>

      <Routes>
        <Route path="/signup" element={<SignUp />} />
        <Route path="/login" element={<LogIn />} />
      </Routes>
    </>
  );
};

export default App;
