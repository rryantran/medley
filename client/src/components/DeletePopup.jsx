import axios from "axios";
import styled from "styled-components";
import Popup from "reactjs-popup";
import Alert from "./Alert";
import { useState } from "react";
import { useUser } from "../hooks/UserHook";
import { HiOutlineTrash } from "react-icons/hi";

const TrashIcon = styled(HiOutlineTrash)`
  color: #000000;
  font-size: 25px;

  &:hover {
    cursor: pointer;
    color: #ffaeb9;
  }
`;

const StyledPopup = styled(Popup)`
  &-overlay {
    background-color: #00000080;
  }
  &-content {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    padding: 40px 20px;
    border-radius: 10px;
    font-family: "Arial", sans-serif;
    background-color: #ffffff;
  }
`;

const Title = styled.div`
  display: inline;
  color: #ffc0cb;
`;

const ButtonContainer = styled.div`
  display: flex;
  flex-direction: row;
  justify-content: space-evenly;
  width: 100%;
`;

const CancelButton = styled.button`
  padding: 10px 0px;
  width: 25%;
  border: none;
  border-radius: 5px;
  background-color: #c0c0c0;
  color: #ffffff;
  font-size: 16px;
  font-weight: bold;
  &:hover {
    background-color: #acacac;
    cursor: pointer;
  }
`;

const DeleteButton = styled.button`
  padding: 10px 0px;
  width: 25%;
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

const CloseButton = styled.button`
  position: absolute;
  top: 5px;
  right: 5px;
  border: none;
  background-color: #00000000;
  font-size: 30px;
  &:hover {
    cursor: pointer;
    color: #ffc0cb;
  }
`;

const DeletePopup = ({ feed, title, fetchFeeds }) => {
  const [open, setOpen] = useState(false);
  const [alert, setAlert] = useState("");
  const [showAlert, setShowAlert] = useState(false);

  const { user } = useUser();

  const handleDelete = () => {
    if (user) {
      axios
        .delete(`/api/user/${user}/feeds/${feed}`, {
          withCredentials: true,
        })
        .then((res) => {
          console.log(res.data);
          fetchFeeds();
          setOpen(false);
        })
        .catch((err) => {
          console.log(err.response.data);
          setAlert(err.response.data.message);
          setShowAlert(true);
        });
    }
  };

  return (
    <>
      <TrashIcon onClick={() => setOpen(true)} />
      <StyledPopup open={open} onClose={() => setOpen(false)} modal={true}>
        <CloseButton onClick={() => setOpen(false)}>&times;</CloseButton>

        <h3>
          Are you sure you want to delete <Title>{title}</Title>?
        </h3>

        <ButtonContainer>
          <DeleteButton onClick={handleDelete}>Delete</DeleteButton>
          <CancelButton onClick={() => setOpen(false)}>Cancel</CancelButton>
        </ButtonContainer>
      </StyledPopup>
    </>
  );
};

export default DeletePopup;
