import axios from "axios";
import { Link, Route, Routes } from "react-router-dom";
import Home from "./pages/Home";
import LogIn from "./pages/LogIn";
import SignUp from "./pages/SignUp";
import NavBar from "./components/NavBar";

const App = () => {
  // test route
  axios.get("/api/user/test").then((result) => {
    console.log(result.data.message);
  });

  return (
    <>
      <NavBar />

      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/signup" element={<SignUp />} />
        <Route path="/login" element={<LogIn />} />
      </Routes>
    </>
  );
};

export default App;
