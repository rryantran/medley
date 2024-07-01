import axios from "axios";
import { useState, useEffect } from "react";
import { useUser } from "../hooks/UserHook";

const Articles = () => {
  const [articles, setArticles] = useState([]);

  const { user } = useUser();

  useEffect(() => {
    if (user) {
      axios
        .get(`/api/user/${user}/articles`)
        .then((res) => {
          console.log(res.data);
          setArticles(res.data);
        })
        .catch((err) => {
          console.log(err);
        });
    }
  }, [user]);

  return (
    <div>
      <h1>Articles</h1>
    </div>
  );
};

export default Articles;
