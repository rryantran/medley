import axios from "axios";
import styled from "styled-components";
import Alert from "../components/Alert";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useUser } from "../hooks/UserHook";

const PageContainer = styled.div`
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding-top: 80px;
  font-family: "Arial", sans-serif;
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

const AddFeed = () => {
  const [title, setTitle] = useState("");
  const [url, setURL] = useState("");
  const [alert, setAlert] = useState("");
  const [showAlert, setShowAlert] = useState(false);

  const navigate = useNavigate();

  const { user } = useUser();

  const handleAddFeed = (e) => {
    e.preventDefault();

    const newFeed = { title, url };

    if (user) {
      axios
        .post(`/api/user/${user}/feeds`, newFeed, { withCredentials: true })
        .then((res) => {
          console.log(res.data);
          navigate("/feeds");
        })
        .catch((err) => {
          console.log(err);
          setAlert(err.response.data.message);
          setShowAlert(true);
        });
    }
  };

  return (
    <PageContainer>
      <h2>Add Feed</h2>

      {showAlert && (
        <Alert
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

        <SubmitButton onClick={handleAddFeed}>Add</SubmitButton>
      </AddFeedForm>
    </PageContainer>
  );
};

export default AddFeed;
