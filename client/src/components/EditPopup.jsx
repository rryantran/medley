import axios from "axios";
import Popup from "reactjs-popup";
import PopupAlert from "./PopupAlert";
import { useState } from "react";
import { useUser } from "../hooks/UserHook";
import { HiOutlinePencil } from "react-icons/hi";

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
      <HiOutlinePencil onClick={() => setOpen(true)} />

      <Popup open={open} onClose={() => setOpen(false)} modal={true}>
        <button
          onClick={() => {
            setOpen(false);
          }}
        >
          &times;
        </button>

        <h2>Update Feed</h2>

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

          <button onClick={handleEdit}>Update</button>
        </form>
      </Popup>
    </>
  );
};

export default EditPopup;
