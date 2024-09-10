import axios from "axios";
import Feed from "../components/Feed";
import AddFeedPopup from "../components/AddFeedPopup";
import { useState, useEffect } from "react";
import { useUser } from "../hooks/UserHook";

const Feeds = () => {
  const [feeds, setFeeds] = useState([]);

  const { user } = useUser();

  useEffect(() => {
    if (user) {
      axios
        .get(`/api/user/${user}/feeds`)
        .then((res) => {
          console.log(res.data);
          setFeeds(res.data);
        })
        .catch((err) => {
          console.log(err);
        });
    }
  }, [user]);

  const fetchFeeds = () => {
    axios
      .get(`/api/user/${user}/feeds`)
      .then((res) => {
        console.log(res.data);
        setFeeds(res.data);
      })
      .catch((err) => {
        console.log(err);
      });
  };

  return (
    <div>
      <h1>Feeds</h1>

      <div>
        <AddFeedPopup fetchFeeds={fetchFeeds} />
      </div>

      <div>
        {feeds.map((feed) => (
          <Feed key={feed.id} feed={feed} fetchFeeds={fetchFeeds} />
        ))}
      </div>
    </div>
  );
};

export default Feeds;
