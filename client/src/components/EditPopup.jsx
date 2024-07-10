import axios from "axios";
import styled from "styled-components";
import Popup from "reactjs-popup";
import PopupAlert from "./PopupAlert";
import { useState } from "react";
import { useUser } from "../hooks/UserHook";
import { HiOutlinePencil } from "react-icons/hi";

const EditIcon = styled(HiOutlinePencil)`
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
    padding: 60px 20px;
    border-radius: 10px;
    font-family: "Arial", sans-serif;
    background-color: #ffffff;
  }
`;

const UpdateFeedForm = styled.form`
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

const EditPopup = ({ feed, fetchFeeds }) => {
  const [title, setTitle] = useState(feed.title);
  const [url, setURL] = useState(feed.url);
  const [alert, setAlert] = useState("");
  const [showAlert, setShowAlert] = useState(false);
  const [open, setOpen] = useState(false);

  const { user } = useUser();

  const handleEdit = (e) => {
    e.preventDefault();

    const updatedFeed = { title, url };

    if (user && (title !== feed.title || url !== feed.url)) {
      axios
        .put(`/api/user/${user}/feeds/${feed.id}`, updatedFeed, {
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
      <EditIcon onClick={() => setOpen(true)} />

      <StyledPopup open={open} onClose={() => setOpen(false)} modal={true}>
        <CloseButton
          onClick={() => {
            setOpen(false);
          }}
        >
          &times;
        </CloseButton>

        <h2>Update Feed</h2>

        {showAlert && (
          <PopupAlert
            message={alert}
            clickHanlder={() => {
              setShowAlert(false);
            }}
          />
        )}

        <UpdateFeedForm>
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

          <SubmitButton onClick={handleEdit}>Update</SubmitButton>
        </UpdateFeedForm>
      </StyledPopup>
    </>
  );
};

export default EditPopup;
