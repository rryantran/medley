import styled from "styled-components";
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

const EditIcon = styled(HiOutlinePencil)`
  color: #000000;
  font-size: 25px;

  &:hover {
    cursor: pointer;
    color: #ffaeb9;
  }
`;

const TrashIcon = styled(HiOutlineTrash)`
  color: #000000;
  font-size: 25px;

  &:hover {
    cursor: pointer;
    color: #ffaeb9;
  }
`;

const Feed = ({ title, url }) => {
  return (
    <ComponentContainer>
      <FeedContainer>
        <FeedTitle>{title}</FeedTitle>
        <FeedLink href={url} target="_blank">
          {url}
        </FeedLink>
      </FeedContainer>
      <ButtonContainer>
        <EditIcon />
        <TrashIcon />
      </ButtonContainer>
    </ComponentContainer>
  );
};

export default Feed;
