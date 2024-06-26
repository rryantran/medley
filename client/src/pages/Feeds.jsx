import axios from "axios";
import styled from "styled-components";
import Feed from "../components/Feed";
import { useState, useEffect } from "react";
import { useUser } from "../hooks/UserHook";

const PageContainer = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  height: 100vh;
  font-family: "Arial", sans-serif;
  background-color: #f5f5f5;
`;

const FeedContainer = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  width: 100%;
`;

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

  return (
    <PageContainer>
      <h2>Feeds</h2>

      <FeedContainer>
        {feeds.map((feed) => (
          <Feed key={feed.id} title={feed.title} url={feed.url} />
        ))}
      </FeedContainer>
    </PageContainer>
  );
};

export default Feeds;
