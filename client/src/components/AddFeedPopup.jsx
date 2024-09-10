import axios from "axios";
import Popup from "reactjs-popup";
import PopupAlert from "./PopupAlert";
import { useState } from "react";
import { useUser } from "../hooks/UserHook";

const AddFeedPopup = ({ fetchFeeds }) => {
  const [title, setTitle] = useState("");
  const [url, setURL] = useState("");
  const [alert, setAlert] = useState("");
  const [showAlert, setShowAlert] = useState(false);
  const [open, setOpen] = useState(false);

  const { user } = useUser();

  const handleAddFeed = (e) => {
    e.preventDefault();

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
          setAlert("");
          setShowAlert(false);
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
      <button onClick={() => setOpen(true)}>Add Feed</button>

      <Popup open={open} onClose={() => setOpen(false)} modal={true}>
        <button
          onClick={() => {
            setOpen(false);
          }}
        >
          &times;
        </button>

        <h2>Add Feed</h2>

        {showAlert && (
          <PopupAlert
            message={alert}
            clickHanlder={() => {
              setShowAlert(false);
            }}
          />
        )}

        <form>
          <input
            type="text"
            placeholder="Feed Title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
          />

          <input
            type="text"
            placeholder="Feed Link"
            value={url}
            onChange={(e) => setURL(e.target.value)}
          />

          <button onClick={handleAddFeed}>Add</button>
        </form>
      </Popup>
    </>
  );
};

export default AddFeedPopup;
