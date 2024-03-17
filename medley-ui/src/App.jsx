import { useState, useEffect } from "react";
import axios from "axios";

const App = () => {
  const [feedLink, setFeedLink] = useState(null);

  useEffect(() => {
    axios.get("/api/feedlinks/1").then((response) => {
      console.log(response.data.url);
      setFeedLink(response.data.url);
    });
  }, []);

  return (
    <>
      <div>{feedLink}</div>
    </>
  );
};

export default App;
