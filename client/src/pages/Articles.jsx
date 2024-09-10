import axios from "axios";
import Article from "../components/Article";
import { useState, useEffect } from "react";
import { useUser } from "../hooks/UserHook";

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
    <div>
      <h2>Articles</h2>

      {loading ? <h3>Fetching your articles...</h3> : ""}

      <div>
        {articles.map((article) => (
          <Article key={article.id} article={article} />
        ))}
      </div>
    </div>
  );
};

export default Articles;
