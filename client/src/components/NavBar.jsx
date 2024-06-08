import styled from "styled-components";
import { Link } from "react-router-dom";

const NavBarContainer = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin: 0;
  padding: 25px 100px;
  border-bottom: 1px solid #c0c0c0;
  font-family: Arial, sans-serif;
`;

const Logo = styled.h1`
  margin: 0;
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
    text-decoration-color: #ffc0cb;
  }
`;

const NavBar = () => {
  return (
    <NavBarContainer>
      <Logo>medley</Logo>

      <LinksContainer>
        <StyledLink to="/">Home</StyledLink>
        <StyledLink to="/login">Log In</StyledLink>
        <StyledLink to="/signup">Sign Up</StyledLink>
      </LinksContainer>
    </NavBarContainer>
  );
};

export default NavBar;
