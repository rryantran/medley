import NavBar from "./components/NavBar";
import AddFeed from "./pages/AddFeed";
import Articles from "./pages/Articles";
import Feeds from "./pages/Feeds";
import Home from "./pages/Home";
import LogIn from "./pages/LogIn";
import SignUp from "./pages/SignUp";
import { Route, Routes } from "react-router-dom";

const App = () => {
  return (
    <>
      <NavBar />

      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/signup" element={<SignUp />} />
        <Route path="/login" element={<LogIn />} />
        <Route path="/articles" element={<Articles />} />
        <Route path="/feeds" element={<Feeds />} />
        <Route path="/addfeed" element={<AddFeed />} />
      </Routes>
    </>
  );
};

export default App;
