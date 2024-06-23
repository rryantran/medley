import styled from "styled-components";
import axios from "axios";
import { Link, useNavigate } from "react-router-dom";
import { useUser } from "../hooks/UserHook";

const NavBarContainer = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin: 0;
  padding: 25px 100px;
  border-bottom: 1px solid #c0c0c0;
  font-family: Arial, sans-serif;
`;

const Logo = styled(Link)`
  margin: 0;
  color: black;
  font-size: 36px;
  font-weight: bold;
  text-decoration: underline;
  text-decoration-thickness: 5px;
  text-decoration-color: #ffc0cb;
`;

const LinksContainer = styled.div`
  display: flex;
  gap: 20px;
`;

const StyledLink = styled(Link)`
  text-decoration: none;
  color: black;
  &:hover {
    text-decoration: underline;
    text-decoration-thickness: 3px;
    text-decoration-color: #ffc0cb;
  }
`;

const LogOut = styled.button`
  margin: 0;
  padding: 0;
  text-decoration: none;
  color: black;
  background-color: transparent;
  border: none;
  font-size: 16px;
  &:hover {
    text-decoration: underline;
    text-decoration-thickness: 3px;
    text-decoration-color: #ffc0cb;
    cursor: pointer;
  }
`;

const NavBar = () => {
  const navigate = useNavigate();
  const { user, setUser } = useUser();

  const handleLogOut = (e) => {
    e.preventDefault();

    axios
      .post("/api/auth/logout")
      .then((result) => {
        console.log(result.data.message);
        setUser(null);
        navigate("/");
      })
      .catch((err) => {
        console.log(err);
      });
  };

  if (user) {
    return (
      <NavBarContainer>
        <Logo to="/">medley</Logo>

        <LinksContainer>
          <StyledLink to="/articles">Articles</StyledLink>
          <StyledLink to="/feeds">Feeds</StyledLink>
          <LogOut onClick={handleLogOut}>Log Out</LogOut>
        </LinksContainer>
      </NavBarContainer>
    );
  } else {
    return (
      <NavBarContainer>
        <Logo to="/">medley</Logo>

        <LinksContainer>
          <StyledLink to="/signup">Sign Up</StyledLink>
          <StyledLink to="/login">Log In</StyledLink>
        </LinksContainer>
      </NavBarContainer>
    );
  }
};

export default NavBar;
