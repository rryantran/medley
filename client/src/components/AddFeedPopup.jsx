import axios from "axios";
import styled from "styled-components";
import Popup from "reactjs-popup";
import PopupAlert from "./PopupAlert";
import { useState } from "react";

const AddFeedButton = styled.button`
  padding: 15px 0px;
  margin: 0px 0px 15px;
  width: 10%;
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

const StyledPopup = styled(Popup)`
  &-overlay {
    background-color: #00000080;
  }
  &-content {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    padding: 60px 20px;
    font-family: "Arial", sans-serif;
    background-color: #ffffff;
  }
`;

const AddFeedForm = styled.form`
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

const CloseButton = styled.button`
  position: absolute;
  top: 10px;
  right: 10px;
  border: none;
  background-color: #00000000;
  font-size: 30px;
  &:hover {
    cursor: pointer;
    color: #ffc0cb;
  }
`;

const AddFeedPopup = ({ user, fetchFeeds }) => {
  const [title, setTitle] = useState("");
  const [url, setURL] = useState("");
  const [alert, setAlert] = useState("");
  const [showAlert, setShowAlert] = useState(false);
  const [open, setOpen] = useState(false);

  const handleAddFeed = () => {
    const newFeed = { title, url };

    if (user) {
      axios
        .post(`/api/user/${user}/feeds`, newFeed, { withCredentials: true })
        .then((res) => {
          console.log(res.data);
          fetchFeeds();
          setOpen(false);
          setTitle("");
          setURL("");
        })
        .catch((err) => {
          console.log(err);
          setAlert(err.response.data.message);
          setShowAlert(true);
        });
    }
  };

  return (
    <>
      <AddFeedButton onClick={() => setOpen(true)}>Add Feed</AddFeedButton>

      <StyledPopup open={open} modal={true}>
        <CloseButton
          onClick={() => {
            setOpen(false);
          }}
        >
          &times;
        </CloseButton>

        <h2>Add Feed</h2>

        {showAlert && (
          <PopupAlert
            message={alert}
            clickHanlder={() => {
              setShowAlert(false);
            }}
          />
        )}

        <AddFeedForm>
          <FormInput
            type="text"
            placeholder="Feed Title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
          />

          <FormInput
            type="text"
            placeholder="Feed Link"
            value={url}
            onChange={(e) => setURL(e.target.value)}
          />

          <SubmitButton
            onClick={(e) => {
              e.preventDefault();
              console.log("hi");
              handleAddFeed();
              close();
            }}
          >
            Add
          </SubmitButton>
        </AddFeedForm>
      </StyledPopup>
    </>
  );
};

export default AddFeedPopup;
