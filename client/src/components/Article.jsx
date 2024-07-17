import styled from "styled-components";

const ComponentContainer = styled.div`
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  width: 65%;
  padding: 20px 40px;
  border: 1px solid #c0c0c0;
  border-radius: 5px;
  background-color: #ffffff;
  box-shadow: 2px 2px #c0c0c0;
`;

const ArticleInfoContainer = styled.div`
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 15px;
`;

const ArticleLink = styled.a`
  color: #ffaeb9;
  font-size: 20px;
`;

const ArticleInfo = styled.p`
  font-size: 15px;
  margin: 0;
`;

const Source = styled.p`
  font-weight: bold;
`;

const Article = ({ article }) => {
  const date = new Date(article.pub_date);
  const formattedDate = date.toLocaleString("en-US", {
    month: "long",
    day: "numeric",
    year: "numeric",
  });

  return (
    <ComponentContainer>
      <ArticleInfoContainer>
        <ArticleLink href={article.url} target="_blank">
          {article.title}
        </ArticleLink>
        <ArticleInfo>By {article.author}</ArticleInfo>
        <ArticleInfo>{formattedDate}</ArticleInfo>
      </ArticleInfoContainer>
      <Source>{article.source}</Source>
    </ComponentContainer>
  );
};

export default Article;
