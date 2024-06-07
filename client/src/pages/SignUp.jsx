import axios from "axios";
import styled from "styled-components";
import { useState } from "react";
import { Link } from "react-router-dom";

const SignUpContainer = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
`;

const Heading = styled.h2`
  font-family: "Arial", sans-serif;
`;

const SignUpForm = styled.form`
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

const LogInPrompt = styled.p`
  margin-top: 20px;
  font-family: "Arial", sans-serif;
  font-size: 14px;
`;

const LogInLink = styled(Link)`
  text-decoration: none;
  color: #ffb6c1;
  &:hover {
    text-decoration: underline;
  }
`;

const SignUp = () => {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();

    const newUser = {
      username: username,
      email: email,
      password: password,
      confirm_password: confirmPassword,
    };

    axios
      .post("/api/auth/signup", newUser)
      .then((res) => {
        console.log(res.data);
      })
      .catch((err) => {
        console.log(err.response.data);
      });
  };

  return (
    <SignUpContainer>
      <Heading>Sign Up</Heading>

      <SignUpForm>
        <FormInput
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        ></FormInput>
        <FormInput
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        ></FormInput>
        <FormInput
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        ></FormInput>
        <FormInput
          type="password"
          placeholder="Confirm Password"
          value={confirmPassword}
          onChange={(e) => setConfirmPassword(e.target.value)}
        ></FormInput>
        <SubmitButton onClick={handleSubmit}>Sign Up</SubmitButton>
      </SignUpForm>

      <LogInPrompt>
        Already have an account? <LogInLink to="/login">Log in</LogInLink>
      </LogInPrompt>
    </SignUpContainer>
  );
};

export default SignUp;
