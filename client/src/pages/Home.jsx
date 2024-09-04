import styled from "styled-components";
import { Link } from "react-router-dom";

const PageContainer = styled.div`
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  width: 50%;
  height: 100%;
  padding: 0;
`;

const Slogan = styled.h2`
  margin-bottom: 0;
  padding: 0;
  font-size: 6rem;
  text-align: center;
`;

const Description = styled.p`
  margin: 3.5rem 0;
  padding: 0;
  text-align: center;
`;

const ButtonContainer = styled.div`
  display: flex;
  gap: 2.5rem;
`;

const SignUpButton = styled(Link)`
  display: flex;
  justify-content: center;
  align-items: center;
  width: 6rem;
  height: 3rem;
  border: 1px solid #ffc0cb;
  border-radius: 5px;
  background-color: white;
  color: #ffc0cb;
  font-size: 1rem;
  font-weight: bold;
  text-decoration: none;

  &:hover {
    background-color: #f8f8f8;
    cursor: pointer;
  }
`;

const LogInButton = styled(Link)`
  display: flex;
  justify-content: center;
  align-items: center;
  width: 6rem;
  height: 3rem;
  border: none;
  border-radius: 5px;
  background-color: #ffc0cb;
  color: white;
  font-size: 1rem;
  font-weight: bold;
  text-decoration: none;

  &:hover {
    background-color: #ffaeb9;
    cursor: pointer;
  }
`;

const Home = () => {
  return (
    <PageContainer>
      <Slogan>Find your perfect blend.</Slogan>

      <Description>
        Aggregate content from all your favorite feeds, all in one place.
      </Description>

      <ButtonContainer>
        <SignUpButton to="/signup">Sign Up</SignUpButton>
        <LogInButton>Log In</LogInButton>
      </ButtonContainer>
    </PageContainer>
  );
};

export default Home;
