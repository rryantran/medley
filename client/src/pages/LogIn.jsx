import axios from "axios";
import styled from "styled-components";
import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import Alert from "../components/Alert";

const PageContainer = styled.div`
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 60vh;
`;

const Heading = styled.h2`
  font-family: "Arial", sans-serif;
`;

const LogInForm = styled.form`
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
  width: 300px;
`;

const FormInput = styled.input`
  padding: 8px 5px;
  width: 85%;
  border-radius: 5px;
  border: 1px solid #c0c0c0;
`;

const SubmitButton = styled.button`
  padding: 15px;
  margin-top: 15px;
  width: 50%;
  border: none;
  border-radius: 5px;
  background-color: #ffc0cb;
  color: #ffffff;
  font-size: 16px;
  font-weight: bold;
  &:hover {
    background-color: #ffaeb9;
    cursor: pointer;
  }
`;

const SignUpPrompt = styled.p`
  margin-top: 20px;
  font-family: "Arial", sans-serif;
  font-size: 14px;
`;

const SignUpLink = styled(Link)`
  text-decoration: none;
  color: #ffb6c1;
  &:hover {
    text-decoration: underline;
  }
`;

const SignUp = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [alert, setAlert] = useState("");
  const [showAlert, setShowAlert] = useState(false);

  const navigate = useNavigate();

  const handleSubmit = (e) => {
    e.preventDefault();

    const user = {
      username: username,
      password: password,
    };

    axios
      .post("/api/auth/login", user)
      .then((res) => {
        console.log(res.data);
        navigate("/");
      })
      .catch((err) => {
        console.log(err.response.data);
        setAlert(err.response.data.message);
        setShowAlert(true);
        setPassword("");
      });
  };

  return (
    <PageContainer>
      <Heading>Log In</Heading>

      {showAlert && (
        <Alert
          message={alert}
          clickHanlder={() => {
            setShowAlert(false);
          }}
        />
      )}

      <LogInForm>
        <FormInput
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        ></FormInput>

        <FormInput
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        ></FormInput>

        <SubmitButton onClick={handleSubmit}>Log In</SubmitButton>
      </LogInForm>

      <SignUpPrompt>
        Don't have an account? <SignUpLink to="/signup">Create one</SignUpLink>
      </SignUpPrompt>
    </PageContainer>
  );
};

export default SignUp;
