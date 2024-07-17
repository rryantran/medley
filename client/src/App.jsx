import styled from "styled-components";
import NavBar from "./components/NavBar";
import Articles from "./pages/Articles";
import Feeds from "./pages/Feeds";
import Home from "./pages/Home";
import LogIn from "./pages/LogIn";
import SignUp from "./pages/SignUp";
import { Route, Routes } from "react-router-dom";

const GlobalContainer = styled.div`
  padding: 95px 0px 45px;
  font-family: Arial, sans-serif;
`;

const App = () => {
  return (
    <>
      <NavBar />

      <GlobalContainer>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/signup" element={<SignUp />} />
          <Route path="/login" element={<LogIn />} />
          <Route path="/articles" element={<Articles />} />
          <Route path="/feeds" element={<Feeds />} />
        </Routes>
      </GlobalContainer>
    </>
  );
};

export default App;
