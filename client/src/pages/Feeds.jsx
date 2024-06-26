import axios from "axios";
import styled from "styled-components";
import Feed from "../components/Feed";
import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
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

const FeedContainer = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  width: 100%;
`;

const Feeds = () => {
  const [feeds, setFeeds] = useState([]);

  const navigate = useNavigate();

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
      <Heading>Feeds</Heading>

      <ButtonContainer>
        <AddFeedButton onClick={() => navigate("/addfeed")}>
          Add Feed
        </AddFeedButton>
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
