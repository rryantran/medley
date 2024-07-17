import styled from "styled-components";
import EditPopup from "./EditPopup";
import DeletePopup from "./DeletePopup";
import { HiOutlinePencil, HiOutlineTrash } from "react-icons/hi";

const ComponentContainer = styled.div`
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  width: 85%;
  padding: 15px 30px;
  border: 1px solid #c0c0c0;
  border-radius: 5px;
  background-color: #ffffff;
  box-shadow: 2px 2px #c0c0c0;
`;

const FeedContainer = styled.div`
  display: flex;
  flex-direction: column;
`;

const FeedTitle = styled.h3`
  margin: 0;
`;

const FeedLink = styled.a`
  width: fit-content;
  color: #ffaeb9;
`;

const ButtonContainer = styled.div`
  display: flex;
  flex-direction: row;
  gap: 15px;
`;

const Feed = ({ feed, fetchFeeds }) => {
  return (
    <ComponentContainer>
      <FeedContainer>
        <FeedTitle>{feed.title}</FeedTitle>

        <FeedLink href={feed.url} target="_blank">
          {feed.url}
        </FeedLink>
      </FeedContainer>

      <ButtonContainer>
        <EditPopup feed={feed} fetchFeeds={fetchFeeds} />
        <DeletePopup feed={feed} fetchFeeds={fetchFeeds} />
      </ButtonContainer>
    </ComponentContainer>
  );
};

export default Feed;
