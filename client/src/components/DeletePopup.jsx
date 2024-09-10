import axios from "axios";
import Popup from "reactjs-popup";
import PopupAlert from "./PopupAlert";
import { useState } from "react";
import { useUser } from "../hooks/UserHook";
import { HiOutlineTrash } from "react-icons/hi";

const DeletePopup = ({ feed, fetchFeeds }) => {
  const [open, setOpen] = useState(false);
  const [alert, setAlert] = useState("");
  const [showAlert, setShowAlert] = useState(false);

  const { user } = useUser();

  const handleDelete = () => {
    if (user) {
      axios
        .delete(`/api/user/${user}/feeds/${feed.id}`, {
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
      <HiOutlineTrash onClick={() => setOpen(true)} />
      <Popup open={open} onClose={() => setOpen(false)} modal={true}>
        <button onClick={() => setOpen(false)}>&times;</button>

        <h3>
          Are you sure you want to delete <Title>{feed.title}</Title>?
        </h3>

        {showAlert && (
          <PopupAlert
            message={alert}
            clickHanlder={() => {
              setShowAlert(false);
            }}
          />
        )}

        <div>
          <button onClick={handleDelete}>Delete</button>
          <button onClick={() => setOpen(false)}>Cancel</button>
        </div>
      </Popup>
    </>
  );
};

export default DeletePopup;
