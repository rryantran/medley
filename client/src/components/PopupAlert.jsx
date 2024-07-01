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
  width: 80%;
`;

const AlertButton = styled.button`
  border: none;
  background-color: #ffc0cb;
  color: #ffffff;
  font-size: 25px;
  &:hover {
    cursor: pointer;
  }
`;

const PopupAlert = ({ message, clickHanlder }) => {
  return (
    <AlertContainer>
      <div>{message}</div>
      <AlertButton onClick={clickHanlder}>&times;</AlertButton>
    </AlertContainer>
  );
};

export default PopupAlert;
