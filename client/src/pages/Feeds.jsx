import axios from "axios";
import styled from "styled-components";
import Feed from "../components/Feed";
import AddFeedPopup from "../components/AddFeedPopup";
import { useState, useEffect } from "react";
import { useUser } from "../hooks/UserHook";

const PageContainer = styled.div`
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding-top: 15px;
  font-family: "Arial", sans-serif;
`;

const Heading = styled.h2`
  margin-bottom: 0px;
`;

const ButtonContainer = styled.div`
  display: flex;
  justify-content: right;
  width: 85%;
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
    <PageContainer>
      <Heading>Feeds</Heading>

      <ButtonContainer>
        <AddFeedPopup user={user} fetchFeeds={fetchFeeds} />
      </ButtonContainer>

      <FeedContainer>
        {feeds.map((feed) => (
          <Feed key={feed.id} title={feed.title} url={feed.url} />
        ))}
      </FeedContainer>
    </PageContainer>
  );
};

export default Feeds;
