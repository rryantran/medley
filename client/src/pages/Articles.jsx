import axios from "axios";
import styled from "styled-components";
import Article from "../components/Article";
import { useState, useEffect } from "react";
import { useUser } from "../hooks/UserHook";

const PageContainer = styled.div`
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding-top: 15px;
`;

const ArticleContainer = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  width: 100%;
`;

const Articles = () => {
  const [articles, setArticles] = useState([]);
  const [loading, setLoading] = useState(true);

  const { user } = useUser();

  useEffect(() => {
    if (user) {
      axios
        .put(`/api/user/${user}/articles`)
        .then((res) => {
          axios.get(`/api/user/${user}/articles`).then((res) => {
            console.log(res.data);
            setArticles(res.data);
            setLoading(false);
          });
        })
        .catch((err) => {
          console.log(err);
        });
    }
  }, [user]);

  return (
    <PageContainer>
      <h2>Articles</h2>

      {loading ? <h3>Fetching your articles...</h3> : ""}

      <ArticleContainer>
        {articles.map((article) => (
          <Article key={article.id} article={article} />
        ))}
      </ArticleContainer>
    </PageContainer>
  );
};

export default Articles;
