import styled from "styled-components";
import { Link } from "react-router-dom";
import { useUser } from "../hooks/UserHook";

const NavBarContainer = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  padding: 2rem 4rem;
  box-sizing: border-box;
  position: fixed;
  border-bottom: 1px solid #c0c0c0;
  font-family: Trebuchet MS, sans-serif;
  background-color: white;
`;

const Logo = styled(Link)`
  color: black;
  font-size: 2.25rem;
  font-weight: bold;
  text-decoration: underline;
  text-decoration-thickness: 5px;
  text-decoration-color: #ffc0cb;
`;

const LinksContainer = styled.div`
  display: flex;
  gap: 2rem;
`;

const StyledLink = styled(Link)`
  text-decoration: none;
  color: black;
  font-size: 1rem;

  &:hover {
    text-decoration: underline;
    text-decoration-thickness: 3px;
    text-decoration-color: #ffc0cb;
  }
`;

const LogOut = styled.p`
  margin: 0;
  text-decoration: none;
  color: black;
  font-size: 1rem;

  &:hover {
    text-decoration: underline;
    text-decoration-thickness: 3px;
    text-decoration-color: #ffc0cb;
    cursor: pointer;
  }
`;

const NavBar = () => {
  const { user, logout } = useUser();

  const handleLogOut = (e) => {
    e.preventDefault();

    logout().catch((err) => {
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
