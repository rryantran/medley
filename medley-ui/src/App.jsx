import { useState, useEffect } from "react";
import axios from "axios";

const App = () => {
  const [data, setData] = useState(null);

  useEffect(() => {
    axios.get("/api/test").then((response) => {
      console.log(response.data.test);
      setData(response.data.test);
    });
  }, []);

  return (
    <>
      <div>{data}</div>
    </>
  );
};

export default App;
