import styled from "styled-components";

const AlertContainer = styled.div`
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  margin: 0px 20px 20px 20px;
  padding: 5px 10px;
  border-radius: 5px;
  background-color: #ffc0cb;
  color: #ffffff;
  font-family: Arial, sans-serif;
  width: 35%;
`;

const AlertButton = styled.button`
  padding: 5px;
  border: none;
  background-color: #ffc0cb;
  color: #ffffff;
  font-size: 18px;
  &:hover {
    cursor: pointer;
  }
`;

const Alert = ({ message, clickHanlder }) => {
  return (
    <AlertContainer>
      <div>{message}</div>
      <AlertButton onClick={clickHanlder}>✕</AlertButton>
    </AlertContainer>
  );
};

export default Alert;
