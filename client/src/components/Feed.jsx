import styled from "styled-components";

const FeedContainer = styled.div`
  display: flex;
  flex-direction: column;
  width: 85%;
  padding: 15px 30px;
  border: 1px solid #c0c0c0;
  border-radius: 5px;
  background-color: #ffffff;
  box-shadow: 2px 2px #c0c0c0;
`;

const FeedTitle = styled.h3`
  margin: 0;
`;

const FeedLink = styled.a`
  color: #ffaeb9;
`;

const Feed = ({ title, url }) => {
  return (
    <FeedContainer>
      <FeedTitle>{title}</FeedTitle>
      <FeedLink href={url}>{url}</FeedLink>
    </FeedContainer>
  );
};

export default Feed;
