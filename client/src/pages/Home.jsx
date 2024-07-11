import styled from "styled-components";

const PageContainer = styled.div`
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 60vh;
`;

const Slogan = styled.h2`
  font-size: 64px;
`;

const Description = styled.p``;

const Home = () => {
  return (
    <PageContainer>
      <Slogan>Find your perfect blend.</Slogan>

      <Description>
        Aggregate content from all your favorite feeds, all in one place.
      </Description>
    </PageContainer>
  );
};

export default Home;
